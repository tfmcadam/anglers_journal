console.log("let\'s go!!")






var map, marker;

function initMap() {
    const coords = { lat: 48.0180914, lng: -122.4605716 };
    var mapOptions = {
        zoom: 8,
        center: coords,
        streetViewControl: false,
        mapTypeControl: false,
        mapTypeId: "satellite"
    }
    
    map = new google.maps.Map(document.getElementById('map'), mapOptions);
    console.log(coords)
    // mylatlng =coords
    // var marker = new google.maps.Marker({
    //     position: mylatlng,
    //     map: map,
    //     title: "yes"
    // });
    // (function (marker, data) {
    //     google.maps.event.addListener(marker, "click", function (e) {
    //         infoWindow.setContent(data,`${one_location.comment}`);
    //         infoWindow.open(map, marker);
    //     });
    // })
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


// function newMarkers(event){
//     console.log('event Linked')
//     event.preventDefault()
// }



// window.onload = function () {
    // }
    // var mapOptions = {
        //     center: new google.maps.LatLng(markers[0].lat, markers[0].lng),
        //     zoom: 8,
        //     mapTypeId: google.maps.MapTypeId.ROADMAP
        // };
        // var infoWindow = new google.maps.InfoWindow();
        // var map = new google.maps.Map(document.getElementById("dvMap"), mapOptions);
        // for (i = 0; i < markers.length; i++) {
            //     var data = markers[i]
            //     var myLatlng = new google.maps.LatLng(data.lat, data.lng);
    //     var marker = new google.maps.Marker({
    //         position: myLatlng,
    //         map: map,
    //         title: data.title
    //     });
    //     (function (marker, data) {
    //         google.maps.event.addListener(marker, "click", function (e) {
    //             infoWindow.setContent(data.description);
    //             infoWindow.open(map, marker);
    //         });
    //     })(marker, data);
    // }
