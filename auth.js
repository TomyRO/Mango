function authRequest() {
  alert('da');
  var iframe = document.createElement('iframe');
  iframe.src = 'https://www.dropbox.com/1/oauth2/authorize?client_id=egdmfyi59f5o2hg&response_type=code&redirect_uri=https://146.148.7.87/&state=MTIzNDU2Nzg5MTExMTExMQ==';

  document.body.appendChild(iframe);
}

document.getElementById("dropbox-submit").onclick = function() {
}
