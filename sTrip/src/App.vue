<template>
  <div>
    <div>
      <nav class="navbar navbar-fixed-top my-navbar" role="navigation">
            <div class="container">
                <div class="navbar-header">
                    <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#example-navbar-collapse">
                          <span class="sr-only">Toggle navigation</span>
                          <span class="icon-bar"></span>
                          <span class="icon-bar"></span>
                          <span class="icon-bar"></span>
                        </button>
                      <div class="navbar-brand" width="100%" >{{title}}</div>
                </div>
                <div class="collapse navbar-collapse nav-style" id="bs-example-navbar-collapse-1">
                    <ul class="nav navbar-nav navbar-right">
                        <ul class="nav navbar-nav">
                            <li><a href="#home" @click="toHome">Home<span class="sr-only">(current)</span></a></li>
                            <li class="dropdown shade">
                                <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">Schemes <span class="caret"></span></a>
                                <ul class="dropdown-menu shade" role="menu">
                                    <li>
                                        <a href="#" @click="currentChange('dangerousHeatMap')">Risk Mapping</a>
                                    </li>
                                    <li class="divider"></li>
                                    <li>
                                        <a href="#" @click="currentChange('infectedPopulationPrediction')"> Close Contacts Tracking</a>
                                    </li>
                                    <li class="divider"></li>
                                    <li>
                                        <a href="#" @click="currentChange('planRoute')">Route Planning</a>
                                    </li>
                                    <li class="divider"></li>

                                </ul>
                            </li>
                            <li data-toggle="modal" data-target="#about"><a href="#" @click="toMine">About Me</a></li>
                            <li data-toggle="modal" data-target="#about"><a href="#">Help</a></li>
                            <li data-toggle="modal" data-target="#about"><a href="#" @click="logout">Logout</a></li>
                        </ul>
                    </ul>
                </div>
            </div>
      </nav>
      <component :is="currentView"
      @main-on-change="mainOnChange" @change-title="navBarTitleChange">
      </component>
    </div>

    <div id="particle"></div>

    <!-- <router-view/> -->
  </div>
</template>

<script>
import mainPage from "./components/mainPage";
import planRoute from "./components/planRoute";
import mine from "./components/mine";
import loginReg from "./components/loginRegister";
import thermogram from "./components/thermogram";
import demo from "./components/demo";
import hotSpot from './components/hotSpot';

export default {
  name: "app",
  components: {
    mainPage,
    planRoute,
    mine,
    loginReg,
    hotSpot,
  },
  data() {
    return {
      mainPage: mainPage,
      currentView: mainPage,
      mine: mine,
      img1: "../static/images/map.jpg",
      logo: "../static/images/logo.png",
      img2: "../static/images/map_ex.png",
      navBarTitle: "Map-Matching",
      activeName: "second",
      isLogin: true,
      title: "sTrip"
    };
  },
  methods: {
    mainOnChange(val) {
      this.currentView = val;
    },
    navBarTitleChange(val) {
      this.title = val;
    },
    loginSuccess(val) {
      this.isLogin = val;
    },
    toMine: function() {
      this.currentView = mine;
      this.title = "Me";
    },
    toHome: function() {
      this.currentView = mainPage;
      this.title = "sTrip";
    },
    logout: function() {
      this.currentView = loginReg;
      this.title = "Login";
    },
    currentChange: function(str) {
      switch (str) {
        case "dangerousHeatMap":
          this.currentView = demo;
          this.title = "Dangerous-Heat-Map";
          break;
        case "infectedPopulationPrediction":
          this.currentView = thermogram;
          this.title = "Infected-Population-Prediction";
          break;
        case "planRoute":
          this.currentView = planRoute;
          this.title = "Route-Planning";
          break;
      }
    }
  },
  watch: {
    title(val) {
      $(".nav-brand").innerHTML = val;
    }
  }
};
</script>

<style scoped>
/* @import "./css/app_css.css"; */

.navbar-brand {
  font-family: "Impact";
  color: #ffffff;
  font-size: 36px;
  margin-left: -130px !important;
}

html,
body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}

body {
  overflow-x: hidden;
  overflow-y: hidden;
  background: white;
}

html {
  widows: 100%;
  position: relative;
  min-height: 100%;
}
/*非常重要的样式让背景图片100%适应整个屏幕*/

.bottom {
  position: absolute;
  bottom: 12%;
}


.shade {
  border-radius: 15px;
}

.my-navbar {
  padding: 20px 0;
  transition: background 0.5s ease-in-out, padding 0.5s ease-in-out;
}

.my-navbar a {
  background: transparent !important;
  color: #e0e0e0 !important;
  font-size: 18px;
  font-family: Helvetica;
  font-weight: 300;
}

.my-navbar a:hover {
  color: #fff !important;
  outline: 0;
}

.my-navbar a {
  transition: color 0.5s ease-in-out;
}
/*-webkit-transition ;-moz-transition*/

.top-nav {
  padding: 0;
  background: #000;
}

button.navbar-toggle {
  background-color: #fbfbfb;
}
/*整个背景都是transparent透明的，会看不到，所以再次覆盖一下*/

button.navbar-toggle > span.icon-bar {
  background-color: #dedede;
}

</style>
