import requests
import json


# Token with permission Zone:Read and DNS:Read on all zones
zone_reader_token = "READER API KEY"
# API token with permission DNS:Edit on all zones
zone_editor_token = "EDITOR API KEY"

# Get current public IP address through ipify.org
current_ip_address = requests.get("https://api.ipify.org", "127.0.0.1").text

def getARecord(zone_id):
	# Execute the API call with the zone_id to get the list of dns records
	dns_response = requests.get("https://api.cloudflare.com/client/v4/zones/{}/dns_records".format(zone_id), 
		headers={"Content-Type":"application/json", "Authorization":"Bearer {}".format(zone_reader_token)})
	# Convert the JSON object to a dict
	dns_response_data = json.loads(dns_response.text)
	print("Got response from DNS API")

	# Iterate through the DNS records in the "result" field of the response
	for result in dns_response_data.get("result"):

		# Check if the DNS record is of type A, if so, put it into the return variable and break
		if result.get("type") == "A":
			# print(result)
			record_id = result.get("id")
			record_name = result.get("name")
			record_content = result.get("content")
			break
	return {"id":record_id,"name":record_name,"content":record_content}

def updateAllZones():
	# Execute API call to get the list of zones
	zones_response = requests.get("https://api.cloudflare.com/client/v4/zones", headers={"Content-Type":"application/json", "Authorization":"Bearer {}".format(zone_reader_token)})
	# Convert JSON to dict
	response_data = json.loads(zones_response.text)
	print("Got response from zones API")

	# print(response_data.get("result")[0])

	# Iterate through the list of zones in the "result" field of the response
	for result in response_data.get("result"):
		# Get the zone ID from the selection
		zone_id = result.get("id")
		# Get the A record ID from the selected zone
		a_record = getARecord(zone_id)
		# print("Record: {}".format(a_record))

		# Send API request editing the record
		edit_response = requests.put("https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}".format(zone_id, a_record["id"]),
			json={"type":"A","name":a_record["name"],"content":current_ip_address,"proxied":True},
			headers={"Content-Type":"application/json", "Authorization":"Bearer {}".format(zone_editor_token)})

		# print(edit_response.text)

		if str(edit_response.status_code)[:1] != "2":
			print("Didn't get a success response!")
		else:
			if a_record["content"] != current_ip_address:
				print("Updated record {} from IP {} to {}.".format(a_record["name"], a_record["content"], current_ip_address))
			else:
				print("Record: {} already has the correct IP address. Not updated.".format(a_record["name"]))


