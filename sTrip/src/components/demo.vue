<template>
  <!--<div class="page">-->
  <div>
    <!--<div v-loading="ifLoadingPath">-->
      <!--<div id="amap_id">-->
        <!--<div id="map-container"> </div>-->
      <!--</div>-->
    <!--</div>-->

    <!--<div id="histogram">-->
      <!--<histogram ref="histogram"></histogram>-->
    <!--</div>-->

    <div id="Gmaps"></div>
    <remote-js
      jsUrl="https://maps.googleapis.com/maps/api/js?key=AIzaSyDrjImDMbNjmkCeMUWkOfq_X0F-56WqUT4&libraries=visualization"
      :js-load-call-back="loadRongJs"
    ></remote-js>

    <el-button-group class="buttongroup">
      <el-button type="primary" size = small icon="el-icon-d-arrow-left" @click.native="loadRongJs(0)">3h</el-button>
      <el-button type="primary" size = small icon="el-icon-d-arrow-left" @click.native="loadRongJs(1)">2.5h</el-button>
      <el-button type="primary" size = small icon="el-icon-d-arrow-left" @click.native="loadRongJs(2)">2h</el-button>
      <el-button type="primary" size = small icon="el-icon-d-arrow-left" @click.native="loadRongJs(3)">1.5h</el-button>
      <el-button type="primary" size = small icon="el-icon-d-arrow-left" @click.native="loadRongJs(4)">1h</el-button>
      <el-button type="primary" size = small icon="el-icon-d-arrow-left" @click.native="loadRongJs(5)">0.5h</el-button>
      <el-button type="primary" size = small icon="el-icon-caret-right" @click="loadRongJs(6)">Refresh</el-button>
    </el-button-group>


    <!--<el-button type="primary" size = small icon="el-icon-d-arrow-left" @click.native="loadRongJs(0)">3h</el-button>-->
    <!--<el-button type="primary" size = small icon="el-icon-d-arrow-left" @click.native="loadRongJs(1)">2.5h</el-button>-->
    <!--<el-button type="primary" size = small icon="el-icon-d-arrow-left" @click.native="loadRongJs(2)">2h</el-button>-->
    <!--<el-button type="primary" size = small icon="el-icon-d-arrow-left" @click.native="loadRongJs(3)">1.5h</el-button>-->
    <!--<el-button type="primary" size = small icon="el-icon-d-arrow-left" @click.native="loadRongJs(4)">1h</el-button>-->
    <!--<el-button type="primary" size = small icon="el-icon-d-arrow-left" @click.native="loadRongJs(5)">0.5h</el-button>-->
    <!--<el-button type="primary" size = small icon="el-icon-caret-right" @click="loadRongJs(6)">Refresh</el-button>-->

    <footer class="bottom">
      <div class="container setFooter">
        <p>Copyright © 2020-2021 HongNiangZi</p>
        <p>版权所有 © 2020-2021 红娘子军团</p>
      </div>
    </footer>

  </div>
</template>

<script>
  import RemoteJs from './remote'
  import axios from 'axios'

  export default {
    components: {RemoteJs},
    props: {},
    data() {
      // randomData: {longitude = 116, latitude = 32, randomData = 'SH'}
      return {
        longitude: 116.31025,
        latitude: 39.9927,
        address: 'SH'
      }
    },
    methods: {
      loadRongJs (index = 0) {
        var options = {
          zoom: 15,
          center: {lat: this.latitude, lng: this.longitude},  // changed
          disableDefaultUI: false,
          zoomControl: true
        }
        var map = new google.maps.Map(document.getElementById('Gmaps'), options)

        mapHeat()

        function mapHeat() {
          /* 热力图 */
          var heatmapData = []
          console.log(index)
          // console.log(heatmapData)

          var points = []

          axios
            .get('http://127.0.0.1:8000/guide/')
            .then(function (response) {
              console.log("get response")
              console.log(response.data)
              // data_ch = JSON.parse(response.data);
              points.push(response.data)
              // points = response.data

              for (var i = 0; i < points[0][index].length; i++) {

                var dict = {location: new google.maps.LatLng(points[0][index][i].lat, points[0][index][i].lng), weight: points[0][index][i].weight}
                heatmapData.push(dict)
              }
              var heatmap = new google.maps.visualization.HeatmapLayer({
                data: heatmapData
              })
              heatmap.setMap(map)
              heatmap.set('radius', 20)
            })

          console.log(points)

        }
      }
    }
  }
</script>


<!--<style rel="stylesheet/scss" lang="scss" scoped>-->
<style>
  @import "../css/style.css";
  @import "../css/app_css.css";
  #Gmaps {
    /*position: absolute;*/
    /*top: 60%;*/
    /*width: 100%;*/
    top: 70px;
    width: 100%;
    height: 34.5rem;
    border-radius: 5px;
  }
  /*#buttongroup{*/
    /*bottom: 10%;*/
  /*}*/
  .my-navbar {
    padding: 0;
    background: #26292f;
    height: 70px;
    padding: 15px;
  }
  .buttongroup{
    position: absolute
  }
  #title {
    font-size: 1.2em;
    color: #26292f;
    /* text-indent: 10px; */
    padding: 5px;
    font-family: "PingFang SC";
    font-weight: 200;
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
  #histogram {
    position: absolute;
    top: 55%;
    width: 100%;
  }
  .el-button-group {
    display: inline-block;
    bottom: 10%;
  }
</style>

