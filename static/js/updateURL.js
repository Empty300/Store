function serializeGet(obj) {
  var str = [];
  for(var p in obj)
    if (obj.hasOwnProperty(p)) {
      str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
    }
  return str.join("&");
}

function addGet(get) {
  get=`page=${get}`
  url = window.location.href
  if (typeof(get) === 'object') {
      get = serializeGet(get);
  }

  if (url.match(/\?/)) {
      document.getElementById("pag").href = url + '&' + get;
  }

  if (!url.match(/\.\w{3,4}$/) && url.substr(-1, 1) !== '/') {
      document.getElementById("pag").href = url + '?' + get;
  }


}