var vue_settings = new Vue({
  el: '#settings_app',
  delimiters: ['[[', ']]'],
  data: {
    address: "",
    netmask: "",
    gateway: "",
    alert: "",
    dns:"",
    module_amount:1,
    u_count:52,
    temp_amount:3
  },
  computed: {
    network_config: function() {
      return { "address": this.address, "netmask": this.netmask, "gateway": this.gateway,"dns":this.dns}
    },
    hardware_config:function(){
      return{"module_amount":this.module_amount,"u_count":this.u_count,"temp_amount":this.temp_amount}
    }


  },
  methods: {
    getNetworkConfig: function() {
      var self = this;
      getAjax('/network', function(data) {
        var data_ = JSON.parse(data);
          self.address = data_.address;
          self.netmask = data_.netmask;
          self.gateway = data_.gateway;
          self.dns = data_.dns;
      });
    },


    getHardwareConfig:function(){
      var self=this;
      getAjax("/hardware-config",function(data){
        var _data=JSON.parse(data);
          self.module_amount=_data.module_amount;
          self.u_count=_data.u_count;
          self.temp_amount=_data.temp_amount;
      })
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
    },

    setHardwareConfig:function(){
      var self=this;
      postAjax("/hardware-config",JSON.stringify(self.hardware_config),function(data){
        var data_ = JSON.parse(data);
        if (data_.status == 'not ok') {
          self.alert = "网络设置没有改动"
        } else {
          self.alert = data_.alert;
        }
      })
    }


  },

  created: function() {
    this.getNetworkConfig();
    this.getHardwareConfig();
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
