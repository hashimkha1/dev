# uat
for testing purposes


# for social login
update site domain in site model using django admin
create social_account for that social platform in django admin where you can add your client_id and client_secret 


# for facebook console developer site(things to remeber)
1> in facebook app top baar activate button is there to activate app
2> to activate app we requied to add privacy policy url which is public and accessible to everyone


# errors:
1. in home page , consultancy and investing page should lead to their respective pages , but they are leading to data Analysis page.
2. in post detail view , if i tried to do delete the post , it is showing system issue
3. in career page , when i try to apply, it is redirecting me to sign up page. is it normal behaviour? i mean how can someone apply for that course?
4. in finance page, 'option' Option in my dashboard section, that page is not working (
    page: https://codamakutano.herokuapp.com/investing/options/shortputdata/
    error: UnboundLocalError at /investing/options/shortputdata/ 
        cannot access local variable 'url_name' where it is not associated with a value
    )

# requirement 257
Question:
1. where to store that investor total share number, amount he/she paid?
- we can use  investor_information table to store the investment details of that user
 but we need to add extra field into that table
  - number_of_share - integer field
  - investment_type - json field(need discussion)
  - investment_document - filefield

email credential
manager@2033
coachofanalytics@gmail.com



production db credential
host: ec2-23-20-224-166.compute-1.amazonaws.com
dbname: d12q1lcmg9u6gm
password: be04d7c0b5040e4a2defff78fc331bdfd085fa91abf1d24e3c3f2bcc8d87ab30
username: avoxjmxvufzjyy