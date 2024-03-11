import etext

sender_credentials = ("definiteconfusioncg@gmail.com", "ekbmohooumnxhxhe")
verifToken = "12345678912345678912"
etext.send_via_email("definiteconfusioncg@gmail.com",
                     f"""Your recovery api call looks like this 
                     \n
                     \n -- Python -- 
                     \nimport requests
                     \nprint(requests.get('http://127.0.0.1:3000/user/verify?token={verifToken}').text)
                     \n
                     \n -- Node.Js -- 
                     \nfetch('http://127.0.0.1:3000/user/verify?token=12345678912345678912')
                     \n.then(response => response.text())
                     \n.then(data => console.log(data))
                     \n.catch(error => console.error('Error:', error));
                     \n
                     \n -- PhP -- 
                    \n<?php
                    \n$url = 'http://127.0.0.1:3000/user/verify?token=12345678912345678912';
                    \n$response = file_get_contents($url);
                    \necho $response;
                    \n?>
""", sender_credentials,
                     "File Host Api Account Recovery")