/**
 * The homepage containing the map view.
 * Author: yueying chang
 * Student id: 1183384
 * Team: COMP90024 - team 24
 */

import 'mapbox-gl/dist/mapbox-gl.css';
//import melb from "./../melb.geojson"
import vic from "./../vicpop.geojson"
import heatmap from "./../heatmap.geojson"
import covidCase from './../case.geojson'
import React from 'react'
import mapboxgl from '!mapbox-gl';// eslint-disable-line import/no-webpack-loader-syntax
import './Home.css'
import PopulationDistributionDonutChart from '../components/PopulationDistributionDonutChart';
import LanguageDistributionBarChart from '../components/LanguageDistributionBarChart';
import Popup from 'reactjs-popup';

mapboxgl.accessToken = 'pk.eyJ1IjoiaW9kYWNoaSIsImEiOiJja29zaGNxbXgwMWllMnhxN201ZXJ0Yjl3In0.6UNecHRhTT17I-PaJOfaNg';
export class Home extends React.Component {
    constructor(props) {
        super(props);
        this.mapContainer = React.createRef();
        this.state = {
            open: false,
            openLanguage: false,
        }
    }

    close = () => {
        this.setState({
            open: false
        })
    }

    closeLanguage = () => {
        this.setState({
            openLanguage: false
        })
    }

    getValueFromParent(nextProps){
        if(this.props.globalStore.scenario !== nextProps.scenario){
            this.isCovid = nextProps.globalStore.scenario === "Victoria Covid"
            this.isHeatmap = nextProps.globalStore.scenario === "Tweet Heatmap"
            this.isLanguages = nextProps.globalStore.scenario === "Languages"
        }
        if(this.props.globalStore.language !== nextProps.language){
            this.selectedLanguage = nextProps.globalStore.language
        }
    }

    componentDidMount() {
        this.selectedLanguage = "ar"
        const map = new mapboxgl.Map({
            container: this.mapContainer.current,
            style: 'mapbox://styles/iodachi/ckosm3m3y2il318mpgeza2axh',
            center: [144.959087, -37.801993],
            zoom: 9,
        });

        map.on('load', function () {
        })
    }

    UNSAFE_componentWillReceiveProps(nextProps){
        this.getValueFromParent(nextProps)
        const map = new mapboxgl.Map({
            container: this.mapContainer.current,
            style: 'mapbox://styles/iodachi/ckosm3m3y2il318mpgeza2axh',
            center: [144.959087, -37.801993],
            zoom: 7,
        });
        var hoveredVicId =  null;

        if (this.isCovid){
        var colors = ['#fed976', '#feb24c', '#fd8d3c', '#fc4e2a', '#e31a1c'];
        map.on('load', function () {  
            fetch("http://172.26.133.226:8000/api/area/tweet")
            .then(res => res.json())
            .then(
                (result) => {
                    this.tweet = result
                },
                (error) => {
                    this.setState({
                        error
                    });
            })

            fetch("http://172.26.133.226:8000/api/area/info")
            .then(res => res.json())
            .then(
                (result) => {
                   this.aurin = result
                },
                (error) => {
                    this.setState({
                        error
                    });
            })

            map.addSource("covid", {
                "type": "geojson",
                "data": covidCase,
                'generateId': true ,
                cluster: true,
                clusterMaxZoom: 14,
                clusterRadius: 50
            });
            
            map.addLayer({
                id: 'clusters',
                type: 'circle',
                source: 'covid',
                filter: ['has', 'point_count'],
                paint: {
                    'circle-color': [
                        'step', ['get', 'point_count'],
                        colors[0],
                        10,
                        colors[1],
                        50,
                        colors[2],
                        100,
                        colors[3],
                        500,
                        colors[4],
                        ],
                    'circle-radius': [
                        'step', ['get', 'point_count'],
                        10,
                        10,
                        20,
                        50,
                        30,
                        100,
                        40
                ]
                }
            });
             
            map.addLayer({
                id: 'cluster-count',
                type: 'symbol',
                source: 'covid',
                filter: ['has', 'point_count'],
                layout: {
                    'text-field': '{point_count_abbreviated}',
                    'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
                    'text-size': 12
                },
                paint: {
                    'text-color': 'white'
                }
             });

             map.addLayer({
                id: 'unclustered-point',
                type: 'circle',
                source: 'covid',
                filter: ['!', ['has', 'point_count']],
                paint: {
                'circle-color': '#11b4da',
                'circle-radius': 4,
                'circle-stroke-width': 1,
                'circle-stroke-color': '#fff'
                }
            });

            map.addSource("vic", {
                "type": "geojson",
                "data": vic,
                'generateId': true 
            });
    
            map.addLayer({
                "id": "vic-fills",
                "type": "fill",
                "source": "vic",
                "layout": {},
                "paint": {
                'fill-color': "#627BC1",
                "fill-opacity": ["case",
                ["boolean", ["feature-state", "hover"], false],
                    0.5,
                    0.1
                ]
                }
            });
             
            map.addLayer({
                "id": "vic-borders",
                "type": "line",
                "source": "vic",
                "layout": {},
                "paint": {
                "line-color": "#627BC1",
                "line-width": 2,
                "line-opacity": 0.4
                }
            });
             
            map.on("mousemove", "vic-fills", (e) => {
                if (e.features.length > 0) {
                if (hoveredVicId) {
                    map.setFeatureState({source: 'vic', id: hoveredVicId}, { hover: false});
                }
                hoveredVicId = e.features[0].id;
                map.setFeatureState({source: 'vic', id: hoveredVicId}, { hover: true});
                }
            });
             
            map.on("mouseleave", "vic-fills", () => {
                if (hoveredVicId) {
                    map.setFeatureState({source: 'vic', id: hoveredVicId}, { hover: false});
                }
                hoveredVicId =  null;
            });
    
            map.on('click', 'vic-fills', (e) => {
                const name = e.features[0].properties.vic_lga__3
                const tweetInfo = this.tweet[e.features[0].properties.vic_lga__3]
                const aurinInfo = this.aurin[e.features[0].properties.vic_lga__3]
                const topWords = tweetInfo ? tweetInfo["hotword"] : "no data"
                const covid = tweetInfo ? tweetInfo["covid_count"] : "no data"
                const crime = tweetInfo ? tweetInfo["crime_count"] : "no data"

                const income = aurinInfo["income"]['median']
                const rent = aurinInfo["rent"]
                const crimeAurin = JSON.stringify(aurinInfo["crime"])

                new mapboxgl.Popup()
                .setLngLat(e.lngLat)
                .setHTML(`<p><strong>${name}</strong><p><b>Top tweeted words: </b>${topWords}</p>
                    <p><b>Covid related tweets: </b>${covid}</p>
                    <p><b>Crime related tweets: </b>${crime}</p>
                    <p><b>Average income / year: </b>${income}</p>
                    <p><b>Average rent / week: </b>${rent}</p>
                    <p><b>Crime count: </b>${crimeAurin}</p></p>`)
                .addTo(map);
            });

            // inspect a cluster on click
            map.on('click', 'clusters', function (e) {
                var features = map.queryRenderedFeatures(e.point, {
                    layers: ['clusters']
                });
                var clusterId = features[0].properties.cluster_id;
                map.getSource('covid').getClusterExpansionZoom(
                    clusterId,
                    function (err, zoom) {
                        if (err) return;
                        map.easeTo({
                            center: features[0].geometry.coordinates,
                            zoom: zoom
                        });
                    });
            });

                map.on('mouseenter', 'clusters', function () {
                    map.getCanvas().style.cursor = 'pointer';
                });
                    
                map.on('mouseleave', 'clusters', function () {
                    map.getCanvas().style.cursor = '';
                });
        });
        
    }else if(this.isHeatmap){
        var colors2 = ['#DFFF00', '#0FFF50', '#4CBB17', '#228B22', '#355E3B', '#023020'];
        map.on('load',  () =>  {
            this.open = false;
            fetch("http://172.26.133.226:8000/api/area/age")
            .then(res => res.json())
            .then(
                (result) => {
                   this.ageInfo = result
                },
                (error) => {
                    this.setState({
                        error
                    });
            })

            map.addSource("vic", {
                "type": "geojson",
                "data": vic,
                'generateId': true 
            });
            map.addLayer({
                "id": "vic-fills",
                "type": "fill",
                "source": "vic",
                "layout": {},
                "paint": {
                'fill-color': [
                        'step', ['get', 'population'],
                        colors2[0],
                        10000,
                        colors2[1],
                        40000,
                        colors2[2],
                        80000,
                        colors2[3],
                        120000,
                        colors2[4],
                        160000,
                        colors2[5],
                        ],
                "fill-opacity": ["case",
                ["boolean", ["feature-state", "hover"], false],
                    0.8,
                    0.5
                ]
                }
            });
             
            map.addLayer({
                "id": "vic-borders",
                "type": "line",
                "source": "vic",
                "layout": {},
                "paint": {
                "line-color": "#627BC1",
                "line-width": 2
                }
            });
            
            map.addSource('heatmap', {
            'type': 'geojson',
            'data': heatmap
            });
             
            map.addLayer(
                {
                'id': 'heat',
                'type': 'heatmap',
                'source': 'heatmap',
                'maxzoom': 9,
                'paint': {
                'heatmap-weight': [
                    'interpolate', ['linear'], ['get', 'mag'], 0, 0, 6, 1],
                'heatmap-intensity': ['interpolate', ['linear'], ['zoom'], 0, 1, 9, 3],
                'heatmap-color': [
                    'interpolate', ['linear'], ['heatmap-density'], 0,
                    'rgba(33,102,172,0)', 0.2, 'rgb(103,169,207)', 0.4,
                    'rgb(209,229,240)', 0.6, 'rgb(253,219,199)', 0.8,
                    'rgb(239,138,98)', 1, 'rgb(178,24,43)'],
                'heatmap-radius': [
                    'interpolate', ['linear'], ['zoom'], 0, 2, 9, 20],
                'heatmap-opacity': [
                    'interpolate', ['linear'], ['zoom'], 7, 1, 9, 0]}
                },
                'waterway-label'
                );
                 
                map.addLayer(
                {
                'id': 'heat-point',
                'type': 'circle',
                'source': 'heatmap',
                'minzoom': 7,
                'paint': {
                'circle-radius': [
                    'interpolate', ['linear'], ['zoom'], 7,
                    ['interpolate', ['linear'], ['get', 'mag'], 1, 1, 6, 4], 16,
                    ['interpolate', ['linear'], ['get', 'mag'], 1, 5, 6, 50]
                ],
                'circle-color': [
                    'interpolate', ['linear'], ['get', 'mag'], 1, 'rgba(33,102,172,0)',
                    2, 'rgb(103,169,207)', 3, 'rgb(209,229,240)', 4, 'rgb(253,219,199)',
                    5, 'rgb(239,138,98)', 6, 'rgb(178,24,43)'],
                'circle-stroke-color': 'white',
                'circle-stroke-width': 1,
                'circle-opacity': [
                    'interpolate', ['linear'], ['zoom'], 7, 0, 8, 1 
                    ]}
                },
                'waterway-label'
                );
             
            map.on("mousemove", "vic-fills", function(e) {
                if (e.features.length > 0) {
                if (hoveredVicId) {
                    map.setFeatureState({source: 'vic', id: hoveredVicId}, { hover: false});
                }
                hoveredVicId = e.features[0].id;
                map.setFeatureState({source: 'vic', id: hoveredVicId}, { hover: true});
                }
            });
             
            map.on("mouseleave", "vic-fills", function() {
                if (hoveredVicId) {
                    map.setFeatureState({source: 'vic', id: hoveredVicId}, { hover: false});
                }
                hoveredVicId =  null;
            });

            map.on('click', 'vic-fills', (e) => {
                this.setState({
                    open: true,
                    chartData: this.ageInfo[e.features[0].properties.vic_lga__3],
                    lgaName: e.features[0].properties.vic_lga__3
                })
            });
            });
    }else if (this.isLanguages){
        map.on('load', () => {  

        fetch("http://172.26.133.226:8000/api/language")
        .then(res => res.json())
        .then(
            (result) => {
                this.languages = result
            },
            (error) => {
        })

        map.addSource("vic", {
            "type": "geojson",
            "data": vic,
            'generateId': true 
        });

        map.addLayer({
            "id": "vic-fills",
            "type": "fill",
            "source": "vic",
            "layout": {},
            "paint": {
            'fill-color': "#627BC1",
            "fill-opacity": ["case",
            ["boolean", ["feature-state", "hover"], false],
                0.5,
                0.1
            ]
            }
        });
         
        map.addLayer({
            "id": "vic-borders",
            "type": "line",
            "source": "vic",
            "layout": {},
            "paint": {
            "line-color": "#627BC1",
            "line-width": 2,
            "line-opacity": 0.4
            }
        });
         
        map.on("mousemove", "vic-fills", (e) => {
            if (e.features.length > 0) {
            if (hoveredVicId) {
                map.setFeatureState({source: 'vic', id: hoveredVicId}, { hover: false});
            }
            hoveredVicId = e.features[0].id;
            map.setFeatureState({source: 'vic', id: hoveredVicId}, { hover: true});
            }
        });
         
        map.on("mouseleave", "vic-fills", () => {
            if (hoveredVicId) {
                map.setFeatureState({source: 'vic', id: hoveredVicId}, { hover: false});
            }
            hoveredVicId =  null;
        });

        map.on('click', 'vic-fills', (e) => {
            this.setState({
                openLanguage: true,
                languageChartData: this.languages[e.features[0].properties.vic_lga__3],
                lgaName: e.features[0].properties.vic_lga__3
            })

            // new mapboxgl.Popup()
            // .setLngLat(e.lngLat)
            // .setHTML(JSON.stringify(this.languages[e.features[0].properties.vic_lga__3]))
            // .addTo(map);
        });
        
        fetch(`http://172.26.133.226:8000/api/language/heatmap/${this.selectedLanguage}`)
        .then(res => res.json())
        .then(
            (result) => {
                this.languageHeatmap = result
            },
            (error) => {
        })

        if(this.languageHeatmap){
            map.addSource('heatmap', {
                'type': 'geojson',
                'data': this.languageHeatmap
                });
                 
                map.addLayer({
                'id': 'heat',
                'type': 'heatmap',
                'source': 'heatmap',
                'maxzoom': 9,
                'paint': {
                'heatmap-weight': [
                    'interpolate', ['linear'], ['get', 'mag'], 0, 0, 6, 1],
                'heatmap-intensity': ['interpolate', ['linear'], ['zoom'], 0, 1, 9, 3],
                'heatmap-color': [
                    'interpolate', ['linear'], ['heatmap-density'], 0,
                    'rgba(33,102,172,0)', 0.2, 'rgb(103,169,207)', 0.4,
                    'rgb(209,229,240)', 0.6, 'rgb(253,219,199)', 0.8,
                    'rgb(239,138,98)', 1, 'rgb(178,24,43)'],
                'heatmap-radius': [
                    'interpolate', ['linear'], ['zoom'], 0, 2, 9, 20],
                'heatmap-opacity': [
                    'interpolate', ['linear'], ['zoom'], 7, 1, 9, 0]}
                },
                'waterway-label'
                );
                 
                map.addLayer({
                'id': 'heat-point',
                'type': 'circle',
                'source': 'heatmap',
                'minzoom': 7,
                'paint': {
                'circle-radius': [
                    'interpolate', ['linear'], ['zoom'], 7,
                    ['interpolate', ['linear'], ['get', 'mag'], 1, 1, 6, 4], 16,
                    ['interpolate', ['linear'], ['get', 'mag'], 1, 5, 6, 50]
                ],
                'circle-color': [
                    'interpolate', ['linear'], ['get', 'mag'], 1, 'rgba(33,102,172,0)',
                    2, 'rgb(103,169,207)', 3, 'rgb(209,229,240)', 4, 'rgb(253,219,199)',
                    5, 'rgb(239,138,98)', 6, 'rgb(178,24,43)'],
                'circle-stroke-color': 'white',
                'circle-stroke-width': 1,
                'circle-opacity': [
                    'interpolate', ['linear'], ['zoom'], 7, 0, 8, 1 
                    ]}
                },
                'waterway-label'
                );
        }
        });
    }
    }
        
    render() {
        return (
            <div>
        <div>
            <div ref={this.mapContainer} className="map-container" />
        </div>
        <div className="popup">
            <Popup open={this.state.open}
            onClose={this.close}>
                <PopulationDistributionDonutChart 
                    data = {this.state.chartData}
                    name = {this.state.lgaName}/>
            </Popup>
        </div>

        <div className="popup">
            <Popup open={this.state.openLanguage}
            onClose={this.closeLanguage}>
                <LanguageDistributionBarChart 
                    data = {this.state.languageChartData}
                    name = {this.state.lgaName}/>
            </Popup>
        </div>
        </div>
        );
    }
}
export default Home;