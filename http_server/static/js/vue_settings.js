var vue_settings = new Vue({
  el: '#settings_app',
  delimiters: ['[[', ']]'],
  data: {
    address: "",
    netmask: "",
    gateway: "",
    alert: "",
    dns:"",

  },
  computed: {
    network_config: function() {
      return { "address": this.address, "netmask": this.netmask, "gateway": this.gateway,"dns":this.dns}
    },


  },
  methods: {
    getNetworkConfig: function() {
      var self = this;
      getAjax('/network', function(data) {
        var data_ = JSON.parse(data);
        if (data_.status == "ok") {
          self.address = data_.data.address;
          self.netmask = data_.data.netmask;
          self.gateway = data_.data.gateway;
          self.dns = data_.data.dns;
        };
      });
    },

    setNetworkConfig: function() {
      var self = this;
      postAjax("/network", JSON.stringify(self.network_config), function(data) {
        var data_ = JSON.parse(data);
        if (data_.status == 'not ok') {
          self.alert = "网络设置没有改动"
        } else {
          self.alert = data_.alert;
        }
      })
    },},

  created: function() {
    this.getNetworkConfig()
  },
})


function getAjax(url, success) {
  var xhr = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
  xhr.open('GET', url);
  xhr.onreadystatechange = function() {
    if (xhr.readyState > 3 && xhr.status == 200) success(xhr.responseText);
  };
  xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  xhr.send();
  return xhr;
};

// example request

function postAjax(url, data, success) {
  var params = typeof data == 'string' ? data : Object.keys(data).map(
    function(k) { return encodeURIComponent(k) + '=' + encodeURIComponent(data[k]) }
  ).join('&');

  var xhr = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");
  xhr.open('POST', url);
  xhr.onreadystatechange = function() {
    if (xhr.readyState > 3 && xhr.status == 200) { success(xhr.responseText); }
  };
  xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.send(params);
  return xhr;
};
