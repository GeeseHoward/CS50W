document.addEventListener('DOMContentLoaded', function () {
        init();
});

function init() {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);
    document.querySelector('#archive').addEventListener('click', archive_mail);
    document.querySelector('#unarchive').addEventListener('click', unarchive_mail);
    document.querySelector('#reply').addEventListener('click', reply);
    document.querySelector('#compose-form .btn').addEventListener('click', send_mail);

    // By default, load the inbox

    load_mailbox('inbox');

    window.onpopstate = function(event) {
        if(event.state != null) {
            console.log(event.state.mailbox);
            if(event.state.tab == 'compose') {
                compose_email();
            }
            else{
                load_mailbox(event.state.tab);
            }
        }
        else{
            history.pushState({tab: 'inbox'}, "", "inbox");
        }
    }

}

function send_mail() {
    recipients = document.querySelector('#compose-recipients').value;
    subject = document.querySelector('#compose-subject').value;
    body = document.querySelector('#compose-body').value;

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);

        // Load Sent Mailbox
        load_mailbox('sent');
    })
    .catch((error) => {
      console.error('Error:', error);
    });

    event.preventDefault();
}


function compose_email() {

    // Push to history
    if(history.state != null){
        if (history.state.tab != "compose"){
            history.pushState({tab: 'compose'}, "", "compose");
        }
    }
    else {
        history.pushState({tab: 'compose'}, "", "compose");
    }


    // Show compose view and hide other views
    document.querySelector('#mailbox-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    document.querySelector('#email-view').style.display = 'none';

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {

    // Push to history
    if(history.state != null){
        if (history.state.tab != mailbox){
            history.pushState({tab: mailbox}, "", `${mailbox}`);
        }
    }
    else {
        history.pushState({tab: mailbox}, "", `${mailbox}`);
    }

    document.querySelector('#emails-list').innerHTML = "";

    // Show the mailbox and hide other views
    document.querySelector('#mailbox-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'none';

    // Show the mailbox name
    document.querySelector('#mailbox-view-heading').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
    document.querySelector('#mailbox-view-heading').style.display = 'block';

    // Print emails

    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
        emails.forEach(email => {

            if(email.archived === true && mailbox !== 'archive'){
                return;
            }

            const element = document.createElement('div');
            element.className = 'container-fluid'
            element.innerHTML = `<div class="row border border-dark">
                                    <div class="col">
                                      <strong>${email.sender}</strong>
                                    </div>
                                    <div class="col-7">
                                      ${email.subject}
                                    </div>
                                    <div class="col-3">
                                      ${email.timestamp}
                                    </div>
                                 </div>`;
            if(email.read === false){
                element.classList.add("unread");
            }

            element.setAttribute('email-id', email.id);
            element.addEventListener('click', view_mail);
            document.querySelector('#emails-list').append(element);

        });
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

function view_mail () {
    // Show the mailbox and hide other views
    document.querySelector('#mailbox-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';
    document.querySelector('#mailbox-view-heading').style.display = 'none';

    email_id = this.getAttribute('email-id');

    root_elem = document.querySelector('#email-view');
    root_elem.setAttribute('email-id', email_id);

    fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
        // Print emails
        console.log(email);
        document.querySelector('#from').innerHTML = email.sender;
        document.querySelector('#to').innerHTML = email.recipients;
        document.querySelector('#subject').innerHTML = email.subject;
        document.querySelector('#timestamp').innerHTML = email.timestamp;
        document.querySelector('#body').innerHTML = email.body.replace(new RegExp('\r?\n','g'), '<br />');

        if(email.read === false) {
            fetch(`/emails/${email.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    read: true
                })
            })
            .then(response => { console.log(response) })
            .catch((error) => {
              console.error('Error:', error);
            });
        }

        if(email.archived === true){
            document.querySelector('#archive').style.display = 'none';
            document.querySelector('#unarchive').style.display = 'block';
        }
        else {
            document.querySelector('#archive').style.display = 'block';
            document.querySelector('#unarchive').style.display = 'none';
        }

    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

function archive_mail() {
    email_id = this.parentElement.parentElement.parentElement.getAttribute('email-id');
    fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: true
        })
    })
    .then(response => {

        console.log(response);
        load_mailbox('inbox');

    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

function unarchive_mail() {

    email_id = this.parentElement.parentElement.parentElement.getAttribute('email-id');
    fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: false
        })
    })
    .then(response => {

        console.log(response);
        load_mailbox('inbox');

    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

function reply() {

    from = document.querySelector('#from').innerHTML;
    to = document.querySelector('#to').innerHTML;
    subject = document.querySelector('#subject').innerHTML;
    timestamp = document.querySelector('#timestamp').innerHTML;
    body = document.querySelector('#body').innerHTML;

    // Show the mailbox and hide other views
    compose_email();

    document.querySelector('#compose-recipients').value = from;
    document.querySelector('#compose-subject').value = 'Re: ' + subject;
    body_new = "\n\n==========\nOn " + timestamp + " " + from +" wrote:" + "\n" + body.replace(/<br\s*[\/]?>/gi, "\n");
    document.querySelector('#compose-body').value = body_new;

}