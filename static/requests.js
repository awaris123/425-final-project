

function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}



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
