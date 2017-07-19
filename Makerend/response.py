""" --- Helpers to build responses which match the structure of the necessary dialog actions --- """

def build_validation_result(is_valid, violated_slot, message_content):
    if message_content is None:
        return {
            "isValid": is_valid,
            "violatedSlot": violated_slot,
        }

    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }





def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }



def get_slots(intent_request):
    return intent_request['currentIntent']['slots']



def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message,
            "responseCard": { 
      "contentType": "application/vnd.amazonaws.card.generic",
      "genericAttachments": [ 
         { 
           
            "buttons": [ 
 
                             { 
                  "text": "Business Hours",
                  "value": "time"
               },
                             { 
                  "text": "Office Address",
                  "value": "Address"
               },
                            { 
                  "text": "Website",
                  "value": "Website"
               },                            { 
                  "text": "Business Name",
                  "value": "Business Name"
               }
            ],
            "imageUrl": "http://www.lambdadivers.org/wp-content/uploads/2016/05/Email-Icon.png",

            "title": "Contact Us"
         },
         { 
            
            "buttons": [ 
               { 
                  "text": "Open Positions",
                  "value": "vacancy"
               }
            ],
            "imageUrl": "http://www.recroit.com/wp-content/uploads/2016/12/HR-Job-Openings-for-Freshers-in-Bangalore_1.png",
            
            "title": "Job Openings"
         },
               { 
            
            "buttons": [ 
               { 
                  "text": "Current Offers",
                  "value": "discount"
               }
            ],
            "imageUrl": "http://easybuysales.com/image/cache/catalog/SpecialOffer-600x600.jpg",
            
            "title": "Offers"
         },
               { 
            
            "buttons": [ 
               { 
                  "text": "Make an appoinment",
                  "value": "appoinments"
               }
            ],
            "imageUrl": "http://presnb.com/wp-content/uploads/2016/05/meeting-image.jpg",
            
            "title": "Appoinments"
         },
               { 
            
            "buttons": [ 
             { 
                  "text": "Regsiter A Complaint",
                  "value": "Complaints"
               }
            ],
            "imageUrl": "https://www.superoffice.com/blog/wp-content/uploads/2013/05/how-to-deal-with-customer-complaints-750x400.jpg",
            
            "title": "Complaint"
         }
      ],
      "version": "44"
   }
        }
    }

    return response
