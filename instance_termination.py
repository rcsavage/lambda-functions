'''AWS Lambda Function::chef-deregister'''
import json
import chef

# Copy the .chef directory into the root folder 
# of the deployment package:

print('Loading chef-deregister function')

def lambda_handler(event, context):
  '''Handler for Lambda'''
  print("Event received: " + json.dumps(event))
  for record in event['Records']:
    if 'Sns' in record:
      message = json.loads(record['Sns']['Message'])
      if message['Event'] == 'autoscaling:EC2_INSTANCE_TERMINATE':
        instance_id = message['EC2InstanceId']
        print("instance_id = " + instance_id)

        try:
          chef_api = chef.autoconfigure()
        except:
          raise Exception('Could not configure Chef!')

        try:
          rows = chef.Search('node', 'ec2_instance_id:' + instance_id)
        except:
          raise Exception('Could not search for nodes with ec2_instance_id: ' + instance_id)

        for row in rows:
          try:
            n = chef.Node(row['name'])
          except:
            raise Exception('Could not fetch node object for ' + row['name'])

          print("chef-node:   " + str(n))

          try:
            c = chef.Client(row['name'])
          except:
            raise Exception('Could not fetch client object for ' + row['name'])

          print("chef-client: " + str(c))

          try:
            n.delete()
          except:
            raise Exception('Could not delete chef-node ' + str(n))

          try:
            c.delete()
          except:
            raise Exception('Could not delete chef-client ' + str(n))

      else:
        raise Exception('Could not process SNS message')
