from troposphere import (
    Base64, GetAtt, FindInMap, Join, Output, Ref, Parameter, Template, constants
)
from troposphere.elasticsearch import (
  Domain, EBSOptions, VPCOptions, ElasticsearchClusterConfig, SnapshotOptions
)
from stacker.blueprints.base import Blueprint

class es_service_domain(Blueprint):
  def create_es_domain(self, ):
    t = self.template
    self.es_domain = t.add_resource(Domain(
      'ElasticsearchDomain',
      DomainName="es-domain-test",
      ElasticsearchClusterConfig=ElasticsearchClusterConfig(
        DedicatedMasterEnabled=False,
        InstanceCount=1,
        ZoneAwarenessEnabled=False,
        InstanceType=constants.ELASTICSEARCH_T2_SMALL
      ),
      EBSOptions=EBSOptions(
        EBSEnabled=True,
        Iops=0,
        VolumeSize=10,
        VolumeType="gp2"
      ),
      ElasticsearchVersion="6.2",
      SnapshotOptions=SnapshotOptions(AutomatedSnapshotStartHour=0),
      AccessPolicies={
        'Version': '2012-10-17',
        'Statement': [{
          'Effect': 'Allow',
          'Principal': {
            'AWS': '*'
          },
          'Action': 'es:*',
          'Resource': '*'
      }]}
    ))
    t.add_output(Output(
      "ElasticSearchDomainName",
      Value=Ref(self.es_domain),
      Description="Name of ES domain for cluster"
    ))

  def create_template(self):
    self.create_es_domain()