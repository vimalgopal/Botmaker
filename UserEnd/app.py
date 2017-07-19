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

    return response.build_validation_result(True, None, None)


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
            global key_id
            val= db_handler(login_id)

            if val > 0 :
                key_id = str(login_id)
                stateof ='logged in'
            else:
                stateof ='no such account'
                val = 'not logged in'
            output_session_attributes['Number'] = stateof  # Elegant pricing model

        return response.delegate(output_session_attributes, response.get_slots(intent_request))

    # Order the flowers, and rely on the goodbye message of the bot to define the message to the end user.
    # In a real bot, this would likely involve a call to a backend service.

    return response.close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Welcome to Lex chatbot'})





""" --- Db Read --- """

def db_handler(id):
    item_count = 0

    with conn.cursor() as cur:
        val=str(id)
        #cur.execute('insert into BussDetails1 (LoginId) values('+val+')')
        conn.commit()
        cur.execute('SELECT * FROM BussDetails1 WHERE LoginId ='+id)
        for row in cur:
            item_count += 1
            #loggerdb.info(row[1])
    return item_count



"""Appoinment"""



""" --- Functions that control the bot's behavior --- """


def get_app(intent_request,key):
    """
    Performs dialog management and fulfillment for getting phone number.
    Beyond fulfillment, the implementation of this intent demonstrates the use of the elicitSlot dialog action
    in slot validation and re-prompting.
    """

    app_purpose = response.get_slots(intent_request)['mpurpose']
    app_day = response.get_slots(intent_request)['mday']
    app_time = response.get_slots(intent_request)['mtime']
    source = intent_request['invocationSource']

    if source == 'DialogCodeHook':
        slots = response.get_slots(intent_request)



        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        if app_purpose is not None and app_day is not None and app_time is not None:

            memail=db_handlerapp(key)


            output_session_attributes['app_state'] = "added to bot"  # Elegant pricing model

        return response.delegate(output_session_attributes, response.get_slots(intent_request))

    # Order the flowers, and rely on the goodbye message of the bot to define the message to the end user.
    # In a real bot, this would likely involve a call to a backend service.
    return response.close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Appoinment Email Sent'})



""" --- Db Write --- """

def db_handlerapp(key):

    item_count = 0


    with conn.cursor() as cur:
        cur.execute("select CompId FROM BussDetails1 where loginId='"+key+"'and AppoState ='yes'")
        conn.commit()
        for row in cur:

            item_count += 1
            loggerdb.info(row[0])

    return (row[0])
    #return "Added %d items from RDS MySQL table" %(item_count)


"""Complaint"""



""" --- Functions that control the bot's behavior --- """


def get_comp(intent_request,key):
    """
    Performs dialog management and fulfillment for getting phone number.
    Beyond fulfillment, the implementation of this intent demonstrates the use of the elicitSlot dialog action
    in slot validation and re-prompting.
    """

    app_purpose = response.get_slots(intent_request)['rcomplaint']
    app_name = response.get_slots(intent_request)['rname']
    app_email = response.get_slots(intent_request)['remail']
    source = intent_request['invocationSource']

    if source == 'DialogCodeHook':
        slots = response.get_slots(intent_request)



        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        if app_purpose is not None and app_name is not None and app_email is not None:

            memail=db_handlerapp(key)


            output_session_attributes['app_state'] = "added to bot"  # Elegant pricing model

        return response.delegate(output_session_attributes, response.get_slots(intent_request))

    # Order the flowers, and rely on the goodbye message of the bot to define the message to the end user.
    # In a real bot, this would likely involve a call to a backend service.
    return response.close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Complaint Registered and confirmation Email Sent'})

"""Address"""


""" --- Functions that control the bot's behavior --- """


def get_caddr(intent_request,key):

    source = intent_request['invocationSource']
    if source == 'DialogCodeHook':





        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

        ad=db_handleraddre(key)
        output_session_attributes['buss_addre'] = ad  # Elegant pricing model

        return response.delegate(output_session_attributes, response.get_slots(intent_request))

    # Order the flowers, and rely on the goodbye message of the bot to define the message to the end user.
    # In a real bot, this would likely involve a call to a backend service.
    return response.close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Business Address Shared'})

def db_handleraddre(key):

    item_count = 0


    with conn.cursor() as cur:
        cur.execute("select BussAddr FROM BussDetails1 where loginId='"+key+"'")
        conn.commit()
        for row in cur:

            item_count += 1
            loggerdb.info(row[0])

    return (row[0])
    #return "Added %d items from RDS MySQL table" %(item_count)



"""Time"""


""" --- Functions that control the bot's behavior --- """


def get_timer(intent_request,key):

    source = intent_request['invocationSource']
    if source == 'DialogCodeHook':





        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

        ad=db_handlertime(key)
        output_session_attributes['buss_addre'] = ad  # Elegant pricing model

        return response.delegate(output_session_attributes, response.get_slots(intent_request))

    # Order the flowers, and rely on the goodbye message of the bot to define the message to the end user.
    # In a real bot, this would likely involve a call to a backend service.
    return response.close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Shared time'})

def db_handlertime(key):

    item_count = 0


    with conn.cursor() as cur:
        cur.execute("select OpenTime FROM BussDetails1 where loginId='"+key+"'")
        conn.commit()
        for row in cur:

            item_count += 1
            loggerdb.info(row[0])

    return (row[0])
    #return "Added %d items from RDS MySQL table" %(item_count)


def get_web(intent_request,key):

    source = intent_request['invocationSource']
    if source == 'DialogCodeHook':





        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

        ad=db_handlerweb(key)
        output_session_attributes['buss_addre'] = ad  # Elegant pricing model

        return response.delegate(output_session_attributes, response.get_slots(intent_request))

    # Order the flowers, and rely on the goodbye message of the bot to define the message to the end user.
    # In a real bot, this would likely involve a call to a backend service.
    return response.close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Shared Website'})

def db_handlerweb(key):

    item_count = 0


    with conn.cursor() as cur:
        cur.execute("select ConWeb FROM BussDetails1 where loginId='"+key+"'")
        conn.commit()
        for row in cur:

            item_count += 1
            loggerdb.info(row[0])

    return (row[0])
    #return "Added %d items from RDS MySQL table" %(item_count)

def get_disc(intent_request,key):

    source = intent_request['invocationSource']
    if source == 'DialogCodeHook':





        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

        ad=db_handlerdisc(key)
        output_session_attributes['buss_addre'] = ad  # Elegant pricing model

        return response.delegate(output_session_attributes, response.get_slots(intent_request))

    # Order the flowers, and rely on the goodbye message of the bot to define the message to the end user.
    # In a real bot, this would likely involve a call to a backend service.
    return response.close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Shared Discount'})

def db_handlerdisc(key):

    item_count = 0


    with conn.cursor() as cur:
        cur.execute("select OfferCode FROM BussDetails1 where loginId='"+key+"'")
        conn.commit()
        for row in cur:

            item_count += 1
            loggerdb.info(row[0])

    return (row[0])
    #return "Added %d items from RDS MySQL table" %(item_count)


def get_job(intent_request,key):

    source = intent_request['invocationSource']
    if source == 'DialogCodeHook':





        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

        ad=db_handlerjob(key)
        output_session_attributes['buss_addre'] = ad  # Elegant pricing model

        return response.delegate(output_session_attributes, response.get_slots(intent_request))

    # Order the flowers, and rely on the goodbye message of the bot to define the message to the end user.
    # In a real bot, this would likely involve a call to a backend service.
    return response.close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Shared Jobs'})

def db_handlerjob(key):

    item_count = 0


    with conn.cursor() as cur:
        cur.execute("select JobWebsite FROM BussDetails1 where loginId='"+key+"'")
        conn.commit()
        for row in cur:

            item_count += 1
            loggerdb.info(row[0])

    return (row[0])
    #return "Added %d items from RDS MySQL table" %(item_count)

""" --- Intents --- """


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']


    # Dispatch to your bot's intent handlers
    if intent_name == 'simpleLoginc':
        return get_number(intent_request)
    if intent_name == 'phoneNumberc':
        return get_num(intent_request,key_id)
    if intent_name == 'appoinmentsc':
        return get_app(intent_request,key_id)
    if intent_name == 'bussNamec':
        return get_buss(intent_request,key_id)
    if intent_name == 'complaintc':
        return get_comp(intent_request,key_id)
    if intent_name == 'conAddc':
        return get_caddr(intent_request,key_id)
    if intent_name == 'conTimec':
        return get_timer(intent_request,key_id)
    if intent_name == 'conWebc':
        return get_web(intent_request,key_id)
    if intent_name == 'discountc':
        return get_disc(intent_request,key_id)
    if intent_name == 'jobWebc':
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
