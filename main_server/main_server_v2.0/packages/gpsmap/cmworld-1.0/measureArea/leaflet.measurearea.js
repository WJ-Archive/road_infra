(function (factory, window) {
  // define an AMD module that relies on 'leaflet'
  if (typeof define === 'function' && define.amd) {
    define(['leaflet'], function (L) {
        factory(L, window.toGeoJSON);
    });

    // define a Common JS module that relies on 'leaflet'
  } else if (typeof exports === 'object') {
    module.exports = function (L) {
      if (L === undefined) {
        if (typeof window !== 'undefined') {
          L = require('leaflet');
        }
      }
      factory(L);
      return L;
    };
  } else if (typeof window !== 'undefined' && window.L) {
    factory(window.L);
  }
}(function (L) {

  function formatNumber(num) {
	    return num.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1,");
	};

	L.Polygon.Area = L.Draw.Polygon.extend({ // L.Polyline.Measure.extend({
	    statics: {
	        TYPE: 'polygon'
	    },

	    Poly: L.Polygon,

	    options: {
	        shapeOptions: {
	            stroke: true,
	            color: '#f06eaa',
	            weight: 4,
	            opacity: 0.5,
	            fill: true,
	            fillColor: null, //same as color by default
	            fillOpacity: 0.2,
	            clickable: true,
	            className : 'areaMeasure'
	        },
	        metric: true, // Whether to use the metric meaurement system or imperial
	        showArea: true, // Whether to display distance in the tooltip
	        calcUnit: 'default'
	    },

	    initialize: function (map, options) {
	        L.Draw.Polygon.prototype.initialize.call(this, map, options);

	        // Save the type so super can fire, need to do this as cannot do this.TYPE :(
	        this.type = L.Draw.Polygon.TYPE;
	    },

	    _startShape: function () {
	        this._drawing = true;
	        this._poly = new L.Polygon([], this.options.shapeOptions);

	        this._container.style.cursor = 'crosshair';

	        this._updateTooltip();
	        this._map.on('mousemove', this._onMouseMove, this);
	    },
	    
	    _finishShape: function () {
	        this._drawing = false;
	        
			var latlngs = this._poly._defaultShape ? this._poly._defaultShape() : this._poly.getLatLngs();
			var intersects = this._poly.newLatLngIntersects(latlngs[latlngs.length - 1]);

			var minx=180, miny=180, maxx=0, maxy=0;
			for (var i=0; i<latlngs.length; i++)
			{
				if (minx > latlngs[i].lng) minx = latlngs[i].lng;
				if (maxx < latlngs[i].lng) maxx = latlngs[i].lng;
				if (miny > latlngs[i].lat) miny = latlngs[i].lat;
				if (maxy < latlngs[i].lat) maxy = latlngs[i].lat;
			}

			var cpt = new L.LatLng((miny + maxy) /2, (minx + maxx) / 2);
			
			if ((!this.options.allowIntersection && intersects) || !this._shapeIsValid()) {
				this._showErrorTooltip();
				return;
			}
			
			this._area = L.GeometryUtil.geodesicArea(latlngs);
			if (!this._poly._areaMarker) {
				this._poly._areaMarker = L.marker(cpt, {
					icon: L.divIcon({
						className: 'leaflet-mouse-marker',
						iconAnchor: [20, 20],
						iconSize: [40, 40]
					}),
					opacity: 0,
					zIndexOffset: this.options.zIndexOffset
				});
				
				this._map.addLayer(this._poly._areaMarker);
			}
			
			var txt = L.GeometryUtil.readableArea(this._area, this.options.metric, this.options.calcUnit);
			this._poly._areaMarker.bindTooltip(txt, {permanent: true, className: "my-label-distance", offset: [10, 0] });
			
			this._fireCreatedEvent();
			this.disable();
	    },
	    
	    _getTooltipText: function () {
	        var showArea = this.options.showArea,
				labelText, distanceStr;

	        if (this._markers.length === 0) {
	            labelText = {
	                text: L.drawLocal.draw.handlers.polyline.tooltip.start
	            };
	        } else if (this._markers.length < 3) {
	            labelText = {
	                text: L.drawLocal.draw.handlers.polyline.tooltip.cont
	            };
	        } else {
	            if (showArea && this._area != undefined) {
	                if (this._area > 1000000) //km로 변환
	                    distanceStr = formatNumber((this._area / 1000000).toFixed(2)) + "㎢";
	                else
	                    distanceStr = formatNumber(this._area.toFixed(2)) + "㎡";
	            }
	            else {
	                distanceStr = '';
	            }

	            labelText = {
	                text: L.drawLocal.draw.handlers.polyline.tooltip.end,
	                subtext: distanceStr
	            };
	        }
	        return labelText;
	    },

	    _shapeIsValid: function () {
	        return this._markers.length >= 3;
	    },
	   
	    _cancelDrawing: function (e) {
	        if (e.keyCode === 27) {
	            disableAreaBtn();
	        }
	    },
	    
	    clearLayers: function (e) {
	    	if (this._markerGroup)
	    	{
	    		this._markerGroup.clearLayers();
	    		this._map.removeLayer(this._markerGroup);
	    		delete this._markerGroup;
	    	}
	    }
	});
  
	L.Control.AreaControl = L.Control.extend({

	    statics: {
	        TITLE: '면적계산'
	    },
	    options: {
	        position: 'topleft',
	        handler: {}
	    },

	    toggle: function () {
	        if (this.handler.enabled()) {
	            this.handler.disable.call(this.handler);
	        } else {
	            this.handler.enable.call(this.handler);
	        }
	    },

	    onAdd: function (map) {
	        var className = 'leaflet-control-draw';

	        var elList = document.getElementsByClassName('leaflet-bar');
	        if (elList.length < 1)
	            this._container = L.DomUtil.create('div', 'leaflet-bar');
	        else
	            this._container = elList[0];

	        this.handler = new L.Polygon.Area(map, this.options.handler);

	        this.handler.on('enabled', function () {
	            L.DomUtil.addClass(this._container, 'enabled');
	        }, this);

	        this.handler.on('disabled', function () {
	            L.DomUtil.removeClass(this._container, 'enabled');
	        }, this);

	        var link = L.DomUtil.create('a', className + '-measure', this._container);
	        link.href = '#';
	        link.title = L.Control.AreaControl.TITLE;

	        L.DomEvent
	            .addListener(link, 'click', L.DomEvent.stopPropagation)
	            .addListener(link, 'click', L.DomEvent.preventDefault)
	            .addListener(link, 'click', this.toggle, this);

	        return this._container;
	    }
	});

  L.Map.mergeOptions({
    areaControl: false
  });


  L.Map.addInitHook(function () {
    if (this.options.areaControl) {
        this.areaControl = L.Control.areaControl().addTo(this);
    }
  });

  L.Control.areaControl = function (options) {
	    return new L.Control.AreaControl(options);
  };
}, window));
