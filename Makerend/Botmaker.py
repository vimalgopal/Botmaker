import math
import dateutil.parser
import datetime
import time
import os
import logging
import sys
import rds_config
import pymysql
import response




rds_host  = "mysqlforlambdatest.c9bcdgowozby.us-east-1.rds.amazonaws.com"
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
loggerdb =logging.getLogger()
loggerdb.setLevel(logging.INFO)

try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=25)
except:
    loggerdb.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()

loggerdb.info("SUCCESS: Connection to RDS mysql instance succeeded")

""" --- Helper Functions --- """


def parse_int(n):
    try:
        return int(n)
    except ValueError:
        return float('nan')


def isValid_num(num):
    try:
        val = int(num)
        return True
    except ValueError:
        return False


def validate_idnum(id):
    if id is not None:
        if not isValid_num(id):
            return response.build_validation_result(False, 'loginId', 'Please re-enter a valid id')
        
    return build_validation_result(True, None, None)


""" --- Functions that control the bot's behavior --- """


def get_number(intent_request):
    """
    Performs dialog management and fulfillment for getting phone number.
    Beyond fulfillment, the implementation of this intent demonstrates the use of the elicitSlot dialog action
    in slot validation and re-prompting.
    """

    login_id = response.get_slots(intent_request)["loginId"]
    source = intent_request['invocationSource']

    if source == 'DialogCodeHook':
        # Perform basic validation on the supplied input slots.
        # Use the elicitSlot dialog action to re-prompt for the first violation detected.
        slots = response.get_slots(intent_request)

        validation_result = validate_idnum(login_id)
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return response.elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])

        # Pass the price of the flowers back through session attributes to be used in various prompts defined
        # on the bot model.
        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        if login_id is not None:
            val=str(login_id)
            db_handler(login_id)
            global key_id
            key_id = val
            output_session_attributes['Number'] = "added to bot"+val  # Elegant pricing model

        return response.delegate(output_session_attributes, response.get_slots(intent_request))

    # Order the flowers, and rely on the goodbye message of the bot to define the message to the end user.
    # In a real bot, this would likely involve a call to a backend service.
    return response.close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Thanks,For providing your id , you are logged in'})



""" --- Db Write --- """

def db_handler(id):
    item_count = 0

    with conn.cursor() as cur:
        val=str(id)
        cur.execute('insert into BussDetails1 (LoginId) values('+val+')')
        conn.commit()
        cur.execute("select * from BussDetails1")
        for row in cur:
            item_count += 1
            loggerdb.info(row)
    return "Added %d items from RDS MySQL table" %(item_count)

"""Phone Number"""

def isValid_num(num):
    try:
        val = int(num)
        return True
    except ValueError:
        return False


def validate_idnum(id):
    if id is not None:
        if not isValid_num(id):
            return response.build_validation_result(False, 'phoneNum', 'Please re-enter a valid id')
        
    return response.build_validation_result(True, None, None)


""" --- Functions that control the bot's behavior --- """


def get_num(intent_request,key):
    """
    Performs dialog management and fulfillment for getting phone number.
    Beyond fulfillment, the implementation of this intent demonstrates the use of the elicitSlot dialog action
    in slot validation and re-prompting.
    """

    phone_num = response.get_slots(intent_request)['phoneNum']
    source = intent_request['invocationSource']

    if source == 'DialogCodeHook':
        slots = response.get_slots(intent_request)

        validation_result = validate_idnum(phone_num)
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return response.elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])

        # Pass the price of the flowers back through session attributes to be used in various prompts defined
        # on the bot model.
        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        if phone_num is not None:
            val=str(phone_num)
            db_handlerphnum(val,key)
            output_session_attributes['PhoneNumber'] = "added to bot"+val  # Elegant pricing model

        return response.delegate(output_session_attributes, response.get_slots(intent_request))

    # Order the flowers, and rely on the goodbye message of the bot to define the message to the end user.
    # In a real bot, this would likely involve a call to a backend service.
    return response.close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Your Business Number have been Added'})



""" --- Db Write --- """

def db_handlerphnum(idn,key):
    item_count = 0

    with conn.cursor() as cur:
        
        
        cur.execute('UPDATE BussDetails1 set PhoneNumber ='+idn+' WHERE LoginId ='+key)
 #       cur.execute('insert into BussDetails (LoginId) values('+id+')')
        conn.commit()
        cur.execute("select * FROM BussDetails1")
        for row in cur:
            item_count += 1
            loggerdb.info(row)
    return "Added %d items from RDS MySQL table" %(item_count)
    


"""Phone Number"""

def isValid_numf(num):
    try:
        val = int(num)
        return False
    except ValueError:
        return True


def validate_app(id):
    if id is not None:
        if not isValid_numf(id):
            return response.build_validation_result(False, 'appState', 'Please enter either yes or no')

    return response.build_validation_result(True, None, None)


""" --- Functions that control the bot's behavior --- """


def get_app(intent_request,key):
    """
    Performs dialog management and fulfillment for getting phone number.
    Beyond fulfillment, the implementation of this intent demonstrates the use of the elicitSlot dialog action
    in slot validation and re-prompting.
    """

    app_state = response.get_slots(intent_request)['appState']
    source = intent_request['invocationSource']

    if source == 'DialogCodeHook':
        slots = response.get_slots(intent_request)

        validation_result = validate_app(app_state)
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return response.elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])

        # Pass the price of the flowers back through session attributes to be used in various prompts defined
        # on the bot model.
        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        if app_state is not None:
            #val=str(app_state)
            db_handlerapp(app_state,key)
            output_session_attributes['app_state'] = "added to bot"+app_state  # Elegant pricing model

        return response.delegate(output_session_attributes, response.get_slots(intent_request))

    # Order the flowers, and rely on the goodbye message of the bot to define the message to the end user.
    # In a real bot, this would likely involve a call to a backend service.
    return response.close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Appoinment Module Updated'})



""" --- Db Write --- """

def db_handlerapp(idn,key):
    item_count = 0

    with conn.cursor() as cur:


        cur.execute("UPDATE BussDetails1 set AppoState ='"+idn+"' WHERE LoginId ="+key)
 #       cur.execute('insert into BussDetails (LoginId) values('+id+')')
        conn.commit()
        cur.execute("select * FROM BussDetails1")
        for row in cur:
            item_count += 1
            loggerdb.info(row)
    return "Added %d items from RDS MySQL table" %(item_count)

"""Business Name"""


def validate_app(id):
    if id is not None:
        if not isValid_numf(id):
            return response.build_validation_result(False, 'bName', 'Please enter your Business Name')

    return response.build_validation_result(True, None, None)


""" --- Functions that control the bot's behavior --- """


def get_buss(intent_request,key):
    """
    Performs dialog management and fulfillment for getting phone number.
    Beyond fulfillment, the implementation of this intent demonstrates the use of the elicitSlot dialog action
    in slot validation and re-prompting.
    """

    buss_name = response.get_slots(intent_request)['bName']
    source = intent_request['invocationSource']

    if source == 'DialogCodeHook':
        slots = response.get_slots(intent_request)

        validation_result = validate_app(buss_name)
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return response.elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])

        # Pass the price of the flowers back through session attributes to be used in various prompts defined
        # on the bot model.
        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        if buss_name is not None:
            #val=str(buss_name)
            db_handlerbus(buss_name,key)
            output_session_attributes['buss_name'] = "added to bot"+buss_name  # Elegant pricing model

        return response.delegate(output_session_attributes, response.get_slots(intent_request))

    # Order the flowers, and rely on the goodbye message of the bot to define the message to the end user.
    # In a real bot, this would likely involve a call to a backend service.
    return response.close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Business Name Updated'})



""" --- Db Write --- """

def db_handlerbus(idn,key):
    item_count = 0

    with conn.cursor() as cur:


        cur.execute("UPDATE BussDetails1 set BusName ='"+idn+"' WHERE LoginId ="+key)
 #       cur.execute('insert into BussDetails (LoginId) values('+id+')')
        conn.commit()
        cur.execute("select * FROM BussDetails1")
        for row in cur:
            item_count += 1
            loggerdb.info(row)
    return "Added %d items from RDS MySQL table" %(item_count)
    
"""Complaint Email"""


def validate_email(id):
    if id is not None:
        if not isValid_numf(id):
            return response.build_validation_result(False, 'comId', 'Please enter a valid email')

    return response.build_validation_result(True, None, None)


""" --- Functions that control the bot's behavior --- """


def get_comp(intent_request,key):
    """
    Performs dialog management and fulfillment for getting phone number.
    Beyond fulfillment, the implementation of this intent demonstrates the use of the elicitSlot dialog action
    in slot validation and re-prompting.
    """

    comp_email = response.get_slots(intent_request)['comId']
    source = intent_request['invocationSource']

    if source == 'DialogCodeHook':
        slots = response.get_slots(intent_request)

        validation_result = validate_email(comp_email)
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return response.elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])

        # Pass the price of the flowers back through session attributes to be used in various prompts defined
        # on the bot model.
        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        if comp_email is not None:
            #val=str(comp_email)
            db_handlercemail(comp_email,key)
            output_session_attributes['comp_email'] = "added to bot"+comp_email  # Elegant pricing model

        return response.delegate(output_session_attributes, response.get_slots(intent_request))

    # Order the flowers, and rely on the goodbye message of the bot to define the message to the end user.
    # In a real bot, this would likely involve a call to a backend service.
    return response.close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Complaint Email Updated'})



""" --- Db Write --- """

def db_handlercemail(idn,key):
    item_count = 0

    with conn.cursor() as cur:


        cur.execute("UPDATE BussDetails1 set CompId ='"+idn+"' WHERE LoginId ="+key)
 #       cur.execute('insert into BussDetails (LoginId) values('+id+')')
        conn.commit()
        cur.execute("select * FROM BussDetails1")
        for row in cur:
            item_count += 1
            loggerdb.info(row)
    return "Added %d items from RDS MySQL table" %(item_count)

"""Address"""


def validate_adress(id):
    if id is not None:
        if not isValid_numf(id):
            return response.build_validation_result(False, 'busAddr', 'Please enter your Business Address')

    return response.build_validation_result(True, None, None)


""" --- Functions that control the bot's behavior --- """


def get_caddr(intent_request,key):
    """
    Performs dialog management and fulfillment for getting phone number.
    Beyond fulfillment, the implementation of this intent demonstrates the use of the elicitSlot dialog action
    in slot validation and re-prompting.
    """

    buss_addre = response.get_slots(intent_request)['busAddr']
    source = intent_request['invocationSource']

    if source == 'DialogCodeHook':
        slots = response.get_slots(intent_request)

        validation_result = validate_adress(buss_addre)
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return response.elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])

        # Pass the price of the flowers back through session attributes to be used in various prompts defined
        # on the bot model.
        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        if buss_addre is not None:
            #val=str(buss_addre)
            db_handleraddre(buss_addre,key)
            output_session_attributes['buss_addre'] = "added to bot"+buss_addre  # Elegant pricing model

        return response.delegate(output_session_attributes, response.get_slots(intent_request))

    # Order the flowers, and rely on the goodbye message of the bot to define the message to the end user.
    # In a real bot, this would likely involve a call to a backend service.
    return response.close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Business Address Updated'})



""" --- Db Write --- """

def db_handleraddre(idn,key):
    item_count = 0

    with conn.cursor() as cur:


        cur.execute("UPDATE BussDetails1 set BussAddr ='"+idn+"' WHERE LoginId ="+key)
 #       cur.execute('insert into BussDetails (LoginId) values('+id+')')
        conn.commit()
        cur.execute("select * FROM BussDetails1")
        for row in cur:
            item_count += 1
            loggerdb.info(row)
    return "Added %d items from RDS MySQL table" %(item_count)
    

"""Time"""

def validate_time(t1,t2):


    if t1 is not None:
        if len(t1) != 5:
            # Not a valid time; use a prompt defined on the build-time model.
            return build_validation_result(False, 'openTime', None)

        hour, minute = t1.split(':')
        hour = parse_int(hour)
        minute = parse_int(minute)
        if math.isnan(hour) or math.isnan(minute):
            # Not a valid time; use a prompt defined on the build-time model.
            return build_validation_result(False, 'openTime', None)
    if t2 is not None:
        if len(t2) != 5:
            # Not a valid time; use a prompt defined on the build-time model.
            return build_validation_result(False, 'closeTime', None)

        hour, minute = t2.split(':')
        hour = parse_int(hour)
        minute = parse_int(minute)
        if math.isnan(hour) or math.isnan(minute):
            # Not a valid time; use a prompt defined on the build-time model.
            return build_validation_result(False, 'closeTime', None)        

    return response.build_validation_result(True, None, None)


""" --- Functions that control the bot's behavior --- """


def get_time(intent_request,key):
    """
    Performs dialog management and fulfillment for getting phone number.
    Beyond fulfillment, the implementation of this intent demonstrates the use of the elicitSlot dialog action
    in slot validation and re-prompting.
    """

    open_time = response.get_slots(intent_request)['openTime']
    close_time = response.get_slots(intent_request)['closeTime']
    source = intent_request['invocationSource']

    if source == 'DialogCodeHook':
        slots = response.get_slots(intent_request)

        validation_result = validate_time(open_time,close_time)
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return response.elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])

        # Pass the price of the flowers back through session attributes to be used in various prompts defined
        # on the bot model.
        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        if open_time is not None and close_time is not None:
            
            #val=str(app_state)
            db_handlertime(open_time,close_time,key)
            output_session_attributes['time'] = "added to bot open"  # Elegant pricing model
        
        return response.delegate(output_session_attributes, response.get_slots(intent_request))

    # Order the flowers, and rely on the goodbye message of the bot to define the message to the end user.
    # In a real bot, this would likely involve a call to a backend service.
    return response.close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Contact Time Updated'})



""" --- Db Write --- """

def db_handlertime(idn,idn1,key):
    item_count = 0

    with conn.cursor() as cur:


        cur.execute("UPDATE BussDetails1 set OpenTime ='"+idn+"' WHERE LoginId ="+key)
        cur.execute("UPDATE BussDetails1 set CloseTime ='"+idn1+"' WHERE LoginId ="+key)
 #       cur.execute('insert into BussDetails (LoginId) values('+id+')')
        conn.commit()
        cur.execute("select * FROM BussDetails1")
        for row in cur:
            item_count += 1
            loggerdb.info(row)
    return "Added %s items from RDS MySQL table" %(idn)

"""Website"""


def validate_web(id):
    if id is not None:
        if not isValid_numf(id):
            return response.build_validation_result(False, 'bussWeb', 'Please enter your website')

    return response.build_validation_result(True, None, None)


""" --- Functions that control the bot's behavior --- """


def get_web(intent_request,key):
    """
    Performs dialog management and fulfillment for getting phone number.
    Beyond fulfillment, the implementation of this intent demonstrates the use of the elicitSlot dialog action
    in slot validation and re-prompting.
    """

    buss_web = response.get_slots(intent_request)['bussWeb']
    source = intent_request['invocationSource']

    if source == 'DialogCodeHook':
        slots = response.get_slots(intent_request)

        validation_result = validate_web(buss_web)
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return response.elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])

        # Pass the price of the flowers back through session attributes to be used in various prompts defined
        # on the bot model.
        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        if buss_web is not None:
            #val=str(buss_web)
            db_handlerweb(buss_web,key)
            output_session_attributes['buss_web'] = "added to bot"+buss_web  # Elegant pricing model

        return response.delegate(output_session_attributes, response.get_slots(intent_request))

    # Order the flowers, and rely on the goodbye message of the bot to define the message to the end user.
    # In a real bot, this would likely involve a call to a backend service.
    return response.close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Business Address Updated'})



""" --- Db Write --- """

def db_handlerweb(idn,key):
    item_count = 0

    with conn.cursor() as cur:


        cur.execute("UPDATE BussDetails1 set ConWeb ='"+idn+"' WHERE LoginId ="+key)
 #       cur.execute('insert into BussDetails (LoginId) values('+id+')')
        conn.commit()
        cur.execute("select * FROM BussDetails1")
        for row in cur:
            item_count += 1
            loggerdb.info(row)
    return "Added %d items from RDS MySQL table" %(item_count)


"""Discounts"""


def validate_dis(id,id1):
    if id is not None:
        if not isValid_numf(id):
            return response.build_validation_result(False, 'offName', 'Please enter your discount offer')
    if id1 is not None:
        if not isValid_numf(id1):
            return response.build_validation_result(False, 'offCode', 'Please enter a discount code')

    return response.build_validation_result(True, None, None)


""" --- Functions that control the bot's behavior --- """


def get_disc(intent_request,key):
    """
    Performs dialog management and fulfillment for getting phone number.
    Beyond fulfillment, the implementation of this intent demonstrates the use of the elicitSlot dialog action
    in slot validation and re-prompting.
    """

    dis_name = response.get_slots(intent_request)['offName']
    dis_code = response.get_slots(intent_request)['offCode']
    source = intent_request['invocationSource']

    if source == 'DialogCodeHook':
        slots = response.get_slots(intent_request)

        validation_result = validate_dis(dis_name,dis_code)
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return response.elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])

        # Pass the price of the flowers back through session attributes to be used in various prompts defined
        # on the bot model.
        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        if dis_name is not None and dis_code is not None:
            #val=str(buss_addre)
            db_handlerdis(dis_name,dis_code,key)
            output_session_attributes['disc'] = "added to bot"  # Elegant pricing model

        return response.delegate(output_session_attributes, response.get_slots(intent_request))

    # Order the flowers, and rely on the goodbye message of the bot to define the message to the end user.
    # In a real bot, this would likely involve a call to a backend service.
    return response.close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Business Address Updated'})



""" --- Db Write --- """

def db_handlerdis(idn,idn1,key):
    item_count = 0

    with conn.cursor() as cur:


        cur.execute("UPDATE BussDetails1 set OfferName ='"+idn+"' WHERE LoginId ="+key)
        cur.execute("UPDATE BussDetails1 set OfferCode ='"+idn1+"' WHERE LoginId ="+key)
 #       cur.execute('insert into BussDetails (LoginId) values('+id+')')
        conn.commit()
        cur.execute("select * FROM BussDetails1")
        for row in cur:
            item_count += 1
            loggerdb.info(row)
    return "Added %d items from RDS MySQL table" %(item_count)





    


"""Job"""


def validate_job(id,id1):
    if id is not None:
        if not isValid_numf(id):
            return response.build_validation_result(False, 'jobOpenWeb', 'Please enter your job openings link')
    if id1 is not None:
        if not isValid_numf(id1):
            return response.build_validation_result(False, 'jobOpenEmail', 'Please enter a valid email id')

    return response.build_validation_result(True, None, None)


""" --- Functions that control the bot's behavior --- """


def get_job(intent_request,key):
    """
    Performs dialog management and fulfillment for getting phone number.
    Beyond fulfillment, the implementation of this intent demonstrates the use of the elicitSlot dialog action
    in slot validation and re-prompting.
    """

    job_web = response.get_slots(intent_request)['jobOpenWeb']
    job_email = response.get_slots(intent_request)['jobOpenEmail']
    source = intent_request['invocationSource']

    if source == 'DialogCodeHook':
        slots = response.get_slots(intent_request)

        validation_result = validate_job(job_web,job_email)
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return response.elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])

        # Pass the price of the flowers back through session attributes to be used in various prompts defined
        # on the bot model.
        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        if job_web is not None and job_email is not None:
            #val=str(buss_addre)
            db_handlerjob(job_web,job_email,key)
            output_session_attributes['job'] = "added to bot"  # Elegant pricing model

        return response.delegate(output_session_attributes, response.get_slots(intent_request))

    # Order the flowers, and rely on the goodbye message of the bot to define the message to the end user.
    # In a real bot, this would likely involve a call to a backend service.
    return response.close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Business Address Updated'})



""" --- Db Write --- """

def db_handlerjob(idn,idn1,key):
    item_count = 0

    with conn.cursor() as cur:


        cur.execute("UPDATE BussDetails1 set JobWebsite ='"+idn+"' WHERE LoginId ="+key)
        cur.execute("UPDATE BussDetails1 set JobEmail ='"+idn1+"' WHERE LoginId ="+key)
 #       cur.execute('insert into BussDetails (LoginId) values('+id+')')
        conn.commit()
        cur.execute("select * FROM BussDetails1")
        for row in cur:
            item_count += 1
            loggerdb.info(row)
    return "Added %d items from RDS MySQL table" %(item_count)



""" --- Main handler --- """

""" --- Intents --- """


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']
    

    # Dispatch to your bot's intent handlers
    if intent_name == 'simpleLogin':
        return get_number(intent_request)
    if intent_name == 'phoneNumber':
        return get_num(intent_request,key_id)
    if intent_name == 'appoinments':
        return get_app(intent_request,key_id)
    if intent_name == 'bussName':
        return get_buss(intent_request,key_id)
    if intent_name == 'complaint':
        return get_comp(intent_request,key_id)
    if intent_name == 'conAdd':
        return get_caddr(intent_request,key_id)
    if intent_name == 'conTime':
        return get_time(intent_request,key_id)
    if intent_name == 'conWeb':
        return get_web(intent_request,key_id)
    if intent_name == 'discount':
        return get_disc(intent_request,key_id)
    if intent_name == 'jobWeb':
        return get_job(intent_request,key_id)
    

    raise Exception('Intent with name ' + intent_name + ' not supported')
    


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))
    
    return dispatch(event)
    
