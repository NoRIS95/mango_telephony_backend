import uvicorn as uvicorn
from fastapi import APIRouter, FastAPI
from mangoapi import MangoAPI
from pydantic import BaseModel

api_vpbx_key = 'ikd2azudhy3ii5q0ewj7vv63uofyq7nw'
api_vpbx_salt = 'kgdcsa56quauuxlr3n8z0mckgrrar4ke'
api_vpbx_url = 'https://app.mango-office.ru/vpbx/'

api = MangoAPI(api_vpbx_url, api_vpbx_key, api_vpbx_salt)

app = FastAPI()

@app.post("/send_sms/")
def send_sms(number:str, text: str, from_ext: str, command_id="base", sender=None):
    return api.sms(number=number, text=text, from_ext=from_ext, command_id=command_id, sender=sender)

@app.post("/callback/")
def make_callback(from_ext: str, to_num: str, command_id="base", from_num=None, line=None, sip_head=None):
    return api.callback(from_ext=from_ext,\
     to_num=to_num, command_id=command_id, from_num=from_num, line=line, sip_head=sip_head)

@app.post("/group_callback/")
def make_group_callback(from_ext: str, to_num: str, command_id="base", line=None):
    return group_callback(from_ext=from_ext, to_num=to_num, command_id=command_id, line=line)

@app.post("/end_call/")
def end_call(call_id: str, command_id="base"):
    return api.hangup(command_id=command_id, call_id=call_id)

@app.post("/start_record/")
def start_record(call_id: str, call_party_number: str, command_id="base"):
    return api.start_record(command_id=command_id, call_id=call_id,
                 call_party_number=call_party_number)

@app.post("/start_play/")
def start_play(call_id: str, internal_id: str, command_id="base", after_play_time=None):
    return api.start_play(call_id=call_id,
               internal_id=internal_id, command_id=command_id, after_play_time=after_play_time)

@app.post("/route_call/")
def route_call(call_id: str, to_number: str, command_id="base", sip_headers=None):
    return api.route(command_id=command_id, call_id=call_id,
          to_number=to_number, sip_headers=sip_headers)

@app.post("/transfer_call/")
def transfer_call(call_id: str, to_number: str, method: str, initiator: str, command_id=None):
    return api.transfer(call_id=call_id, to_number=to_number, method=method,
             initiator=initiator, command_id=command_id)

@app.post("/get_stats_to/")
def get_stats_to(to_ext: str, date_from: int, date_to: int, fields: str, to_num=None, request_id=None):
    return api.get_stats_to(to_ext=to_ext, date_from=date_from, date_to=date_to,
                 fields=fields, to_num=to_num, request_id=request_id)

@app.post("/get_stats_from/")
def get_stats_from(from_ext: str, date_from: int, date_to: int, fields: str, from_num=None, request_id=None):
    return api.get_stats_from(from_ext=from_ext, date_from=date_from, date_to=date_to,
                 fields=fields, from_num=from_num, request_id=request_id)

@app.post("/get_stats_call_party/")
def get_stats_call_party(call_party_ext: str, date_from: int, date_to: int, fields: str, call_party_num=None, request_id=None):
    return api.get_stats_call_party(call_party_ext=call_party_ext, date_from=date_from, date_to=date_to,
                         fields=fields, call_party_num=call_party_num, request_id=request_id)

@app.post("/get_dct_user_info/")
def get_dct_user_info(number: str):
    return api.dct_user_info(number=number)

@app.post("/get_dct_user_history/")
def get_dct_user_history(number: str):
    return api.dct_user_history(number=number)


@app.post("/user_list") #РАБОТАЕТ
def get_user_list(ext_fields=None, extension=None):
    fields_list = ["general.user_id", "general.sips", "groups", "general.access_role_id", "telephony.dial_alg",
               "telephony.numbers.schedule", "telephony.line_id", "telephony.trunk_number_id", "general.mobile",
               "general.login", "general.use_status", "general.use_cc_numbers"]
    return api.user_list(ext_fields=fields_list, extension=extension)

@app.post("/group_list")
def get_group_list(group_id=None, operator_id=None, operator_extension=None, show_users=1):
    return api.group_list(group_id=group_id, operator_id=operator_id,\
        operator_extension=operator_extension, show_users=show_users)

@app.post("/balance")
def get_balance():
    return api.balance()

@app.post("/lines")
def get_lines():
    return api.lines()

@app.post("/audio")
def get_audio():
    return api.audio()

@app.post("/set_schema")
def set_schema(schema: int, line: int, trunk=None):
	return api.set_schema(schema=schema, line=line, trunk=trunk)

@app.post("/get_ext_field")
def get_ext_field(ext_fields=None):
	return api.schemas(ext_fields=ext_fields)

@app.post("/roles")
def get_roles():
    return api.roles()

@app.post("/sips_list")
def get_sips_list():
    return api.sips_list()

@app.post("/domains_list")
def get_domains_list():
    return api.domains_list()

@app.post("/trunk_num_list") 
def get_trunk_num_list():
    return api.trunk_num_list()

@app.post("/bwlist_state")
def get_bwlist_state():
    return api.bwlist_state()

@app.post("/bwlist_nums")
def get_bwlist_nums():
    return api.bwlist_nums()

@app.post("/add_bwlist")
def add_bwlist(number: str, list_type='white', num_type='tel', comment='API'):
    return api.bwlist_add(number=number, list_type=list_type, num_type=num_type, comment=comment)

@app.delete("/delete_bwlist")
def delete_bwlist(num_id: int):
    return api.bwlist_del(num_id=num_id)


@app.post("/campaign_info")
def get_campaign_info(campaign_id: int):
    return api.campaign_info(campaign_id=campaign_id)

@app.post("/ab_contact_init")
def make_ab_contact_init(query: str, limit_rows: int, order=None, contact_ext_fields=None):
    return api.ab_contact_init(query=query, limit_rows=limit_rows, order=order, contact_ext_fields=contact_ext_fields)


@app.post("/cc_deal_list") 
def get_cc_deal_list(product_id: int, status: str, from_date=None, until_date=None,
                     members_ids=None, contact_id=None):   
	return api.cc_deal_list(product_id=product_id, status=status, from_date=from_date,
        until_date=until_date, members_ids=members_ids, contact_id=contact_id)

@app.post("/cc_deal_funnels_list")
def get_cc_deal_funnels_list(product_id: int):   
    return api.cc_deal_funnels_list(product_id=product_id)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)