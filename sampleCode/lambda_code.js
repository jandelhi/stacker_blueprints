/*
 * Sample node.js code for AWS Lambda to get Apache log files from S3, parse
 * and add them to an Amazon Elasticsearch Service domain.
 *
 */

/* Imports */
var AWS = require('aws-sdk');
var path = require('path');

/* Globals */
var esDomain = {
    endpoint: process.env.ES_ENDPOINT,
    region: 'us-east-1',
    index: process.env.ES_INDEX,
    doctype: process.env.ES_DOCTYPE
};
var endpoint =  new AWS.Endpoint(esDomain.endpoint);

/*
 * The AWS credentials are picked up from the environment.
 * They belong to the IAM role assigned to the Lambda function.
 * Since the ES requests are signed using these credentials,
 * make sure to apply a policy that permits ES domain operations
 * to the role.
 */
var creds = new AWS.EnvironmentCredentials('AWS');


/*
 * Add the given document to the ES domain.
 * If all records are successfully added, indicate success to lambda
 * (using the "context" parameter).
 */
function postDocumentToES(doc, context) {
    var req = new AWS.HttpRequest(endpoint);

    req.method = 'POST';
    req.path = path.join('/', esDomain.index, esDomain.doctype);
    req.region = esDomain.region;
    req.body = doc;
    req.headers['presigned-expires'] = false;
    req.headers['Host'] = endpoint.host;

    // Sign the request (Sigv4)
    var signer = new AWS.Signers.V4(req, 'es');
    signer.addAuthorization(creds, new Date());

    // Post document to ES
    var send = new AWS.NodeHttpClient();
    send.handleRequest(req, null, function(httpResp) {
        var body = '';
        httpResp.on('data', function (chunk) {
            body += chunk;
        });
        httpResp.on('end', function (chunk) {
          context.succeed();
        });
    }, function(err) {
        console.log('Error: ' + err);
        context.fail();
    });
}

/* Lambda "main": Execution starts here */
  exports.handler = (event, context) => {
    console.log('Received event: ', JSON.stringify(event, null, 2));
    event.Records.forEach((record) => {
        console.log('Stream record: ', JSON.stringify(record, null, 2));
        if (record.eventName == 'INSERT') {
          var movie = {
            "movieID": JSON.stringify(record.dynamodb.NewImage.Id.S),
            "movieTitle": JSON.stringify(record.dynamodb.NewImage.Name.S),
            "movieRating": JSON.stringify(record.dynamodb.NewImage.Rating.N)}
          postDocumentToES(movie, context);
        }
    });
  };   