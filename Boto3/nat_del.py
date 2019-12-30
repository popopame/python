import boto3
#This Lambda will delete a NAT GW and release the associated EIP based on a provided tag
#The lambda need to be improved , so that more than one NAT can be deleted


#Edit the Value , so that it correspond to the tag-key of your NGW
filter=[{'Name': 'tag-key','Values': ['nat']}]
ec2 = boto3.client('ec2')

#This function will return the nat_ID correspond to the nat GW with the tag-key nat
#Need to be modified so it can return a list if there is more than on NAT GW
def get_nat_id(custom_filter):

    natgw_id=ec2.describe_nat_gateways(Filters=custom_filter)

    for nat in natgw_id["NatGateways"]:
        nat_id= nat["NatGatewayId"]

    return nat_id


#Will Delete the NAT GW with the ID provided by the get_nat_id function
def del_nat(nat_id):
    response = ec2.delete_nat_gateway(NatGatewayId=str(nat_id))
    return response

#Will release the EIP associated with the NAT Gateway
def release_eip(custom_filter):
    natgw_id=ec2.describe_nat_gateways(Filters=custom_filter)

    for nat in natgw_id["NatGateways"]:
        for nerf_nat in nat["NatGatewayAddresses"]:
            response = ec2.release_address(AllocationId=str(nerf_nat["AllocationId"]),)
            return response





print (release_eip(filter))
print (del_nat(get_nat_id(filter)))
