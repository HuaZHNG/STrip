<template>
  <div class="page">
    <div v-loading="ifLoadingPath">
      <div id="amap_id">
        <table border="1" id='table-infected'>
            <tr>
              <th>Personal ID</th>
              <th>Status</th>
              <th>Contact Place</th>
            </tr>
            <tr v-for="tableInfo in tableInfos">
                <td>{{ tableInfo.ID }}</td>
                <td>{{ tableInfo.Status }}</td>
                <td>{{ tableInfo.Place}}</td>
            </tr>
        </table>
      </div>
    </div>


    <div id="histogram">
      <histogram ref="histogram"></histogram>
    </div>
    <nav class="main-menu" style="z-index: 12; overflow: hidden;">
      <ul id="pickers">
        <li>
          <div id="descrip">ENTER CONFIRMED PERSONAL ID
            <!--<el-tooltip effect="dark" content="Click here to add this route to favourites" placement="bottom">-->
            <!--</el-tooltip>-->
          </div>
        </li>
        <li>
        <div id="descrip2">
          <div id="search-box"> <br>
            <i class="icon-locate"></i>
            <input class="start" id="start" type="text" name="start" @keyup.enter="enterEnterStart" placeholder="Personal ID" >
          </div>
          </div>
        </li>
      </ul>

      <div id="descrip1">
        <el-tooltip effect="dark" content="Click here to track close contacts" placement="bottom">
            <el-button size="small" id="submit" class="collect" type="text" style="position: relative; left: 17%;
            color: black" @click="contact"> DONE </el-button>
        </el-tooltip>
      </div>
    </nav>
    <footer class="bottom">
      <div class="container setFooter">
        <p>Copyright © 2020-2021 HongNiangZi</p>
        <p>版权所有 © 2020-2021 红娘子军团</p>
      </div>
    </footer>
  </div>
</template>
<script>
  import picker from "./picker.vue";
  import addPicker from "./addPicker.vue";
  import AMap from "AMap";
  import AMapUI from "AMapUI";
  import segmentLocations from '../assets/py/edge_geometry.json';


  export default {
    data() {
      let self = this;
      return {
        zoom: 16,
        center: [116.3059, 39.9869],
        map: null,
        pois: [],
        markers: [],
        pickers: [],
        flags: [],
        arriveTime: [],
        departureTime: [],
        currentPathId: [],
        edgeGeometry: segmentLocations.edgeGeometry,
        ifLoadingPath: false,
        directionsService: null,
        directionsRenderer: null,
        geocoder: null,
        // tableInfos:[{
        //   'ID':'xx',
        //   'Status': 'good',
        //   'Place':'20180101'
        // },{
        //   'ID':'xx',
        //   'Status': 'good',
        //   'Place':'20200202'
        // }]
        tableInfos:[],
        request: 0
      };
    },
    mounted() {
      //this.initMap1();
      this.pickers.push(0);
      this.flags.push({
        value: true,
        key: 0,
        placeholder:"start"
      });
      this.pickers.push(1);
      this.flags.push({
        value: true,
        key: 1,
        placeholder:"end"
      });

    },
    methods: {
      initMap1: function() {
        self.directionsService = new google.maps.DirectionsService;
        self.directionsRenderer = new google.maps.DirectionsRenderer;
        var map = new google.maps.Map(document.getElementById('amap_id'), {
          zoom: this.zoom,
          center: {lat: this.center[1], lng: this.center[0]}
        });
        self.map = map;
        self.infowindow = new google.maps.InfoWindow();
        self.geocoder = new google.maps.Geocoder();
        directionsRenderer.setMap(map);
      },
      contact: function() {
        console.log(document.getElementById('start').value)
        self.request = document.getElementById('start').value
        axios
          .get('http://127.0.0.1:8000/contact/', {params: {key: self.request}})
          .then(function (response) {
            console.log("get response")
            console.log(response.data)
            // data_ch = JSON.parse(response.data);
            // points.push(response.data)
            // points = response.data

            var ID = []

            ID.push(response.data)
            console.log(ID.length)
            for (var i=0; i<ID.length; i++){
              console.log(ID[0][i])
            }
          })
      }
    }
  }
</script>

<style>
  @import "../css/style.css";
  @import "../css/app_css.css";
  .my-navbar {
    padding: 0;
    background: #26292f;
    height: 70px;
    padding: 15px;
  }
  #favourite {
    position: relative;
    left: 48%;
    cursor: pointer;
    top: 0%;
    transition: all 0.4s;
  }
  #favouriteImg {
    position: relative;
  }
  #favouriteImg:hover {
    transform: scale(1.2);
  }
  #title {
    font-size: 1.2em;
    color: #26292f;
    /* text-indent: 10px; */
    padding: 5px;
    font-family: "PingFang SC";
    font-weight: 200;
  }
  #detail {
    font-size: 0.2rem;
    color: #424242;
    margin-top: -20px;
    margin-right: 25px;
  }
</style>


<style scoped>
  .setFooter {
    background: #26292f;
    height: 90px;
    width: 900%;
    position: relative;
    top: 104px;
    z-index: 13;
    padding: 0px;
  }
  .setFooter p {
    position: relative;
    left: 40px;
    top: 18px;
    color: white;
    font-weight: 200;
    font-family: Helvetica Neue;
    font-size: 13px;
  }
  #descrip {
    position: relative;
    left: 16%;
    font-family: "Impact";
    font-size: 1.2em;
    top: 20px;
    /* margin: 5px; */
  }
  #descrip1 {
    position: relative;
    left: 25%;
    font-family: "Impact";
    font-size: 1.2em;
    top: 5%;
    /* margin: 5px; */
  }
  #descrip2 {
    font-family: "Impact";
    font-size: 1.2em;
  }
  #histogram {
    position: absolute;
    top: 55%;
    width: 100%;
  }
  .collect {
    transition: all 0.4s;
  }
  .collect:hover {
    transform: scale(1.2);
  }
  #search-box {
    position: relative;
    width: 180px;
    height: 70px;
    top: 29px;
    left: 25px;
    font-size: 4px;
    color: #26282D;
    font-weight: 250;
  }
  .start {
    position: relative;
    width: 220px;
    height: 32px;
    border: none;
    box-shadow: 2px 2px 5px #CBCBCB;
    padding-inline-start: 30px;
    padding-inline-end: 20px;
  }
  .end {
    position: relative;
    width: 220px;
    height: 32px;
    border: none;
    box-shadow: 2px 2px 5px #CBCBCB;
    padding-inline-start: 30px;
    padding-inline-end: 20px;
    top: 15px;
  }
  .icon-locate {
    position: absolute;
    left: 8px;
    z-index: 5;
    margin-top: 8px;
    background-image: url('../../static/images/定位.png');
    /*引入图片图片*/
    background-repeat: no-repeat;
    /*设置图片不重复*/
    background-position: 0px 0px;
    /*图片显示的位置*/
    width: 40px;
    /*设置图片显示的宽*/
    height: 35px;
    /*图片显示的高*/
  }
  #table-infected {
    margin: 80px;
  }
</style>
