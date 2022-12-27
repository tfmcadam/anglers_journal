
console.log("script linked")

var map, marker;

function initMap() {
    const coords = { lat: 48.0180914, lng: -122.4605716 };
    var mapOptions = {
        zoom: 8,
        center: coords,
        streetViewControl: false,
        mapTypeId: "satellite"
    }

    map = new google.maps.Map(document.getElementById('map'), mapOptions);
    console.log(coords)

    var searchBox = new google.maps.places.SearchBox(document.getElementById('pac-input'));

    map.controls[google.maps.ControlPosition.TOP_CENTER].push(document.getElementById('pac-input'));
    google.maps.event.addListener(searchBox, 'places_changed', function () {
        searchBox.set('map', null);


        var places = searchBox.getPlaces();

        var bounds = new google.maps.LatLngBounds();
        var i, place;
        for (i = 0; place = places[i]; i++) {
            (function (place) {
                var my_latLng = place.geometry.location
                var lat = my_latLng.lat()
                var lng = my_latLng.lng()
                
                document.getElementById('lat').value = lat
                document.getElementById('lng').value = lng
                var marker = new google.maps.Marker({
                    
                    position: place.geometry.location,
                    draggable: true
                });
    
                // marker.bindTo('map', searchBox, 'map');
                google.maps.event.addListener(marker, 'map_changed', function () {
                    
                    console.log(lat, lng)

                    document.getElementById('lat').value = lat
                    document.getElementById('lng').value = lng
                    
                    if (!this.getMap()) {
                        this.unbindAll();
                    }
                });
                bounds.extend(place.geometry.location);
                
                
            }(place));
            console.log(place.geometry.location)
            
        }
        map.fitBounds(bounds);
        searchBox.set('map', map);
        map.setZoom(Math.min(map.getZoom(), 12));
        
    });
    // let markerOptions = {
    //     position: coords,
    //     map: map,
    //     title: "new marker",
    //     draggable: true,
    //     optimized: false
    // }
    
    function addMarker(props) {
        document.getElementById('lat').value = props.coords.lat()
        document.getElementById('lng').value = props.coords.lng()
        if (marker) {
            marker.setPosition(props.coords);
        } else {
            marker = new google.maps.Marker({
                position: props.coords,
                map: map,
                animation: google.maps.Animation.DROP,
            });
        }
        }
    google.maps.event.addListener(map, 'click',
        function (event) {
            var my_latLng = event.latLng;
            // var lat = my_latLng.lat();
            // var lng = my_latLng.lng();
            console.log(event.latLng)
            addMarker({
                coords: event.latLng,
                content:
                    `
                ANY CONTENT YOU WANT ON INFO WINDOW GOES HERE, HTML TOO
                `});
        });
    function getId() {
        fetch('/get_id')
            .then(response => response.json())
            .then(data => {
                console.log(data);
                for (let i = 0; i < data.length; i++) {
                    lat = data[i].lat
                    lng = data[i].lng
                    coordobj = { lat: parseFloat(lat), lng: parseFloat(lng) }
                    // console.log(lat + ',' + lng)
                    // console.log(lat)
                    // console.log(lng)
                    addSavedMarkers({
                        coords: coordobj
                    })
                }
            })
    }
    getId();

    function addSavedMarkers(props) {
        console.log(props.coords)
        marker = new google.maps.Marker({
            position: props.coords,
            map: map,

            animation: google.maps.Animation.DROP
        })
    }
    function getData() {
        fetch('/get_data')
            .then(response => response.json())
            .then(data => {
                for (let i = 0; i < data.length; i++) {
                    lat = data[i].lat
                    lng = data[i].lng
                    coordobj = { lat: parseFloat(lat), lng: parseFloat(lng) }
                    // console.log(lat + ',' + lng)
                    // console.log(lat)
                    // console.log(lng)
                    addSavedMarkers({
                        coords: coordobj
                    })
                }
            })
    }
    // Prints out { message : "Hello World" }
    getData();

    function addSavedMarkers(props) {
        console.log(props.coords)
        marker = new google.maps.Marker({
            position: props.coords,
            map: map,
            animation: google.maps.Animation.DROP
        })
    }


}

