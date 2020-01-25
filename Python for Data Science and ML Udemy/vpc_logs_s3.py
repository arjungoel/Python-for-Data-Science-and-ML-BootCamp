import boto3

def get_cloudwatch_log_groups(global_vars):
    """
    Get the list of Cloudwatch Log groups
    :param global_vars: The list of global variables
    :param type: json
    :return: resp_data Return a dictionary of data, includes list of 'log_groups'
    :rtype: json
    """
    resp_data = {'status': False, 'log_groups':[], 'error_message': ''}
    client = boto3.client('logs')
    try:
        # Lets get all the logs
        resp = client.describe_log_groups( limit = 50 )
        resp_data['log_groups'].extend( resp.get('logGroups') )
        # Check if the results are paginated
        if resp.get('nextToken'):
            while True:
                resp = client.describe_log_groups( nextToken = resp.get('nextToken'), limit = 50 )
                resp_data['log_groups'].extend( resp.get('logGroups') )
                # Check & Break, if the results are no longer paginated
                if not resp.get('nextToken'):
                    break
        resp_data['status'] = True
    except Exception as e:
        resp_data['error_message'] = str(e)
    return resp_data

def filter_logs_to_export(global_vars, lgs):
    """
    Get a list of log groups to export by applying filter
    :param global_vars: The list of global variables
    :param type: json
    :param lgs: The list of CloudWatch Log Groups
    :param type: json
    :return: resp_data Return a dictionary of data, includes list of filtered 'log_groups'
    :rtype: json
    """
    resp_data = {'status': False, 'log_groups':[], 'error_message': ''}
    # Lets filter for the logs of interest
    for lg in lgs.get('log_groups'):
        if lg.get('logGroupName') in global_vars.get('cw_logs_to_export'):
            resp_data['log_groups'].append(lg)
            resp_data['status'] = True
    return resp_data
