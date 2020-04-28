



function signup(){
  const baseURL = "http://127.0.0.1:5000"
  var form = document.forms["signup"]
  var fname = form.elements['fname'].value
  var lname = form.elements['lname'].value
  var jobtype = form.elements['jobtype'].value
  var ssn = form.elements['SSN'].value

  console.log(fname)
  console.log(lname)
  console.log(jobtype)

  data={
    fname:fname,
    lname:lname,
    jobtype:jobtype,
    ssn:ssn
  }

  json = JSON.stringify(data)

  form.reset();
  $.ajax({
    contentType: 'application/json',
    type: "POST",
    url: "http://127.0.0.1:5000" + "/employee",
    data: json,
    success: function(data){
        console.log("it worked!");
      },
      dataType: "json"
    });



}
