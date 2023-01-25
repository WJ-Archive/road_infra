var map, map2, map3, map4, m_ActiveMapContainer;
var body;
var ui = {};
var m_showInformation = false;
var m_showInformationBuild = false;
var m_maxLevel = 15;
var m_CustomLayers = [];
var m_CustomLayerNames = [];
var gbn;
var m_MinZoom = 11;
var m_MaxZoom = 18;

var m_GRS80CRS;


//배경지도 설정
function setBackgroundMap(bEmap, year) {
	if (bEmap == true) {
		//항공사진 레이어 삭제
		for (var id in map._layers) {
			if (!map._layers[id]._url) continue;
			
			if (map._layers[id]._url.indexOf('/dj_') > 0)
				map.removeLayer(map._layers[id]);
		}
		
		$('#mapid').css('background-color', 'white');
		L.tileLayer.CmWorld('/cmworld2d/map/{z}/{x}/{y}.png', {
            crs: L.TileLayer.CmWorld.GetUTMKCRS(),
            minzoom: 10,
            maxZoom: m_MaxZoom,
            maxNativeZoom: 21,
            tileSize: 256,
            tms: true,
         }).addTo(map);
		$('.map-cont').hide();
	} 
	
	//지적경계 색상 변경
	if (map.cmvLayer) {
		var partname = 'etc';
		if (map.cmvLayer[partname]) {
			var style = getLayerStyle('연속지적도', partname);
			if (style) {
				var layerinfo = map.cmvLayer[partname].LayerInfos[style.LayerID];
				 //라인 스타일과 두께 변경
				if (bEmap==false && layerinfo.Renderer.renderItem[0].strokestyle.indexOf('rgba(0') == 0) {
					layerinfo.Renderer.renderItem[0].strokestyle = "rgba(255, 255, 0, 1)";
					layerinfo.Renderer.renderItem[0].strokewidth = 1;
					
					refreshMap();
				} else if (bEmap==true && layerinfo.Renderer.renderItem[0].strokestyle.indexOf('rgba(255') == 0) {
					layerinfo.Renderer.renderItem[0].strokestyle = "rgba(0, 0, 0, 0.3)";
					layerinfo.Renderer.renderItem[0].strokewidth = 0.3;
					
					refreshMap();
				}
			}
		}
	}
}
// CRS
function GetGRS80TMMiddleCRS(){
   var crs = new L.Proj.CRS(
      'EPSG:5186', 
      '+proj=tmerc +lat_0=38 +lon_0=127 +k=1 +x_0=200000 +y_0=600000 +ellps=GRS80 +units=m +no_defs ');
   return crs;
}

//지도 초기화
function init__map() {
	if (!m_GRS80CRS) m_GRS80CRS = GetGRS80TMMiddleCRS(); 

	// options126.63330298464308, 36.85071954110766
	var latlng = new L.LatLng(36.76777, 126.63330); // new refined center
	var northEast = new L.LatLng(37.1, 127.3); //128.059051); // set maxBounds
	var southWest = new L.LatLng(36.7, 126); //36.562385
	window.bounds = new L.LatLngBounds(southWest, northEast);
	window.latlng = latlng;

	var iMapLevel = 11;
	
	map = L.map('mapid', {
	       crs: L.TileLayer.CmWorld.GetUTMKCRS(),//
	       bounds: [[36.562385, 126.036791], [37.089875, 128.059051]], // 지도 범위
	       continuousWorld: false,
	       worldCopyJump: false,
	       minZoom: m_MinZoom, // 최소 줌레벨
	       maxZoom: m_MaxZoom, // 최대 줌레벨
	       maxBounds: window.bounds,  // 최대 지도 범위
	       zoomControl: false, // 줌컨트롤 사용여부
	       renderer : L.svg() // 렌더러 
	    }).setView(latlng);
	
	if (!initMapViewRange()){
		latlng = new L.LatLng(36.84476, 126.64707);
    	map.setView(latlng, iMapLevel);
    }
	
    //배경지도
	setBackgroundMap(true);
	// style
	readTextFile("/cmworld2d/resources/json/maps_cmv.json", function(text){
	    var data = JSON.parse(text);
	    m_LayerList = data;
	});

	var onePixelResolution = 0.078125000000000000;
	map.on('click', function (e) {
		
		var lat = e.latlng.lat;
		var lon = e.latlng.lng;
		
	    var level = map.getZoom();
	    
	    var tmpPt = map.options.crs.project(e.latlng);
	    console.log(level + ": (" + e.latlng.lng + ', ' + e.latlng.lat + ') UTMK (' + tmpPt.x.toString() + "," + tmpPt.y.toString() + ")");
	    
	   
	});
	map.on("zoomend", function (e) {
    	console.log(e._zoom);
    });

}
// json 파일 읽기
function readTextFile(file, callback) {
    var rawFile = new XMLHttpRequest();
    rawFile.overrideMimeType("application/json");
    rawFile.open("GET", file, true);
    rawFile.onreadystatechange = function() {
        if (rawFile.readyState === 4 && rawFile.status == "200") {
            callback(rawFile.responseText);
        }
    }
    rawFile.send(null);
}

//LocalStorage에서 지난 번 지도 범위 가져옴.  
function initMapViewRange(){
	var view = localStorage['mapView'];
  	
  	if (!view) return false;
	view = JSON.parse(view || '');
	if (view.lng) {
		if ((map.options.bounds[0][0] < view.lat && view.lat < map.options.bounds[1][0])
				&& (map.options.bounds[0][1] < view.lng && view.lng < map.options.bounds[1][1]))
			{
				map.setView(L.latLng(view.lat, view.lng), view.zoom, true);
				return true;
			}
		}

  return false;
}
//LocalStorage에서 지난 번 지도 범위 가져옴.  
function oncmvdraw(cmvlayer, state) {
}

//cmv 레이어정보 구하기
function getLayerStyle(layername, partname) {
	var lid = -1;
	for (var id in m_LayerList) {
		if (partname) {
			if (m_LayerList[id].part1.toLowerCase() == partname && m_LayerList[id].layername == layername) {
				lid = id;
				break;
			}
		} else {
			if (m_LayerList[id].layername == layername) {
				lid = id;
				break;
			}
		}
	}
	
	if (lid < 0) return;
	
	var style = {"LayerID": m_LayerList[lid].layerid, "LayerName": m_LayerList[lid].layername, "ThematicStyle":m_LayerList[lid].thematicstyle,"ThematicKey":m_LayerList[lid].thematickey,
			"LabelVisible": m_LayerList[lid].labelvisible,"FontFamily": m_LayerList[lid].fontfamily, "FontFillColorA": m_LayerList[lid].fontfillcolora, 
			"FontFillColorR":m_LayerList[lid].fontfillcolorr,"FontFillColorG":m_LayerList[lid].fontfillcolorg,"FontFillColorB":m_LayerList[lid].fontfillcolorb, 
			"FontOutlineColorA": m_LayerList[lid].fontoutlinecolora,"FontOutlineColorR": m_LayerList[lid].fontoutlinecolorr,"FontOutlineColorG":m_LayerList[lid].fontoutlinecolorg,
			"FontOutlineColorB":m_LayerList[lid].fontoutlinecolorb,"FontOutlineWidth":m_LayerList[lid].fontoutlinewidth,"FontOutlineJoin":m_LayerList[lid].fontoutlinejoin,
			"FontOutlineMiterLimit":m_LayerList[lid].fontoutlinemiterlimit,"FontTextAlign":m_LayerList[lid].fonttextalign, "FontVerticalAlign": m_LayerList[lid].fontverticalalign,
			"LineStyle" : m_LayerList[lid].linestyle, "LineColorA": m_LayerList[lid].linecolora, "LineColorR":m_LayerList[lid].linecolorr, 
			"LineColorG": m_LayerList[lid].linecolorg, "LineColorB": m_LayerList[lid].linecolorb, "LineWidth": m_LayerList[lid].linewidth,
			"FillColorA": m_LayerList[lid].fillcolora,"FillColorR": m_LayerList[lid].fillcolorr,"FillColorG": m_LayerList[lid].fillcolorg,"FillColorB": m_LayerList[lid].fillcolorb,
			"Visible": true, "SymbolName": m_LayerList[lid].symbolname, 
			"TableName": m_LayerList[lid].tablename, "Selectable": m_LayerList[lid].selectable};

	return style;
}

//지도를 다시 그림
function refreshMap(visible) {
	var cpt = map.getCenter();
	if(visible) {
		cpt.lat = cpt.lat - 0.0000000002;
	} else {
		cpt.lat = cpt.lat + 0.0000000002;
	}
    
    map.setView(cpt, map.getZoom());
}





































function getCmvLayerByName(layername) {
	if (!map.cmvLayer) return;
	
	for (var id in map.cmvLayer.LayerNames) {
		if (map.cmvLayer.LayerNames[id].layername == layername) 
			return map.cmvLayer.LayerNames[id];
	}
}

function getCmvLayer(layerID) {
	if (!map.cmvLayer) return;
	
	for (var id in map.cmvLayer.LayerInfos) {
		if (map.cmvLayer.LayerInfos[id].layername == layername) 
			return map.cmvLayer.LayerNames[id];
	}
}





