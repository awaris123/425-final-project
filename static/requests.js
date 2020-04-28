



function signup(){
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


  $.ajax({
    contentType: 'application/json',
    type: "POST",
    url: "http://127.0.0.1:5000/employee",
    data: JSON.stringify(data),
    success: function(data){
        window.location.replace("http://127.0.0.1:5000"+data);
      },
      error : function(xhr, textStatus, errorThrown) {
          console.log(xhr, textStatus, errorThrown)
          alert('An error occurred!');
      },
      dataType: "html"
    });
}

function login(){

  var form = document.forms["login"]
  var eID = form.elements["eID"].value
  document.cookie = "eID="+eID
  console.log(eID)
  window.location.replace("http://127.0.0.1:5000/home/"+eID)

}
