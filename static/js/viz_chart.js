const AXIS_MAPPER = {
        NS: "x",
        EW: "y",
        UD: "z",
        ns: "x",
        ew: "y",
        ud: "z",
        X: "x",
        Y: "y",
        Z: "z",
        x: "x",
        y: "y",
        z: "z",
    },
    X_AXIS_DATA = [
        2.0e-2,
        2.18101547e-2,
        2.37841423e-2,
        2.59367911e-2,
        2.82842712e-2,
        3.08442165e-2,
        3.36358566e-2,
        3.66801617e-2,
        4.0e-2,
        4.36203093e-2,
        4.75682846e-2,
        5.18735822e-2,
        5.65685425e-2,
        6.1688433e-2,
        6.72717132e-2,
        7.33603235e-2,
        8.0e-2,
        8.72406186e-2,
        9.51365692e-2,
        1.03747164e-1,
        1.13137085e-1,
        1.23376866e-1,
        1.34543426e-1,
        1.46720647e-1,
        1.6e-1,
        1.74481237e-1,
        1.90273138e-1,
        2.07494329e-1,
        2.2627417e-1,
        2.46753732e-1,
        2.69086853e-1,
        2.93441294e-1,
        3.2e-1,
        3.48962474e-1,
        3.80546277e-1,
        4.14988657e-1,
        4.5254834e-1,
        4.93507464e-1,
        5.38173706e-1,
        5.86882588e-1,
        6.4e-1,
        6.97924949e-1,
        7.61092554e-1,
        8.29977315e-1,
        9.0509668e-1,
        9.87014928e-1,
        1.07634741,
        1.17376518,
        1.28,
        1.3958499,
        1.52218511,
        1.65995463,
        1.81019336,
        1.97402986,
        2.15269482,
        2.34753035,
        2.56,
        2.7916998,
        3.04437021,
        3.31990926,
        3.62038672,
        3.94805971,
        4.30538965,
        4.6950607,
        5.12,
        5.58339959,
        6.08874043,
        6.63981852,
        7.24077344,
        7.89611943,
        8.61077929,
        9.3901214,
        1.024e1,
        1.11667992e1,
        1.21774809e1,
        1.3279637e1,
        1.44815469e1,
        1.57922389e1,
        1.72215586e1,
        1.87802428e1,
        2.048e1,
        2.23335984e1,
        2.43549617e1,
        2.65592741e1,
        2.89630938e1,
        3.15844777e1,
        3.44431172e1,
        3.75604856e1,
        4.096e1,
        4.46671967e1,
        4.87099234e1,
        5.31185482e1,
        5.79261875e1,
        6.31689554e1,
        6.88862343e1,
        7.51209712e1,
        8.192e1,
        8.93343935e1,
        9.74198469e1,
        1.06237096e2,
        1.15852375e2,
        1.26337911e2,
        1.37772469e2,
        1.50241942e2,
        1.6384e2,
        1.78668787e2,
        1.94839694e2,
        2.12474193e2,
        2.3170475e2,
        2.52675822e2,
        2.75544937e2,
        3.00483885e2,
        3.2768e2,
        3.57337574e2,
        3.89679387e2,
        4.24948385e2,
        4.634095e2,
        5.05351643e2,
        5.51089875e2,
        6.0096777e2,
        6.5536e2,
    ];

var isBase = true,
    width = 300,
    height = 150,
    margin = {
        top: 10,
        right: 20,
        bottom: 20,
        left: 40,
    };

function changeLayout() {
    if (!isBase) {
        base_layout();
        isBase = true;
    }
}

function base_layout() {
    $("#sensor-loc-map").css({
        width: "100%",
    });

    $("#info").css({
        display: "none",
    });
}

/**
 *  Set markers on the map and
 *  set listener for each marker data
 *
 *  @param {Array.Object} sensors The sensors set on the map
 *  @param {<google.maps.Map>} map The map set markers
 *  @return {Array.<google.maps.Marker>}
 *  @todo use real url
 */
function sensorStatusToMarker(heartbeat, triggered) {
    marker_base = "/static/images/markers/";
    if (triggered && (Date.parse(triggered) > Date.parse(new Date()) - 30000)) { // 30sec
        return marker_base + "marker_red.png";
    } else if (heartbeat && (Date.parse(heartbeat) > Date.parse(new Date()) - 120000)) { //2min
        return marker_base + "marker_green.png";
    } else if (heartbeat && (Date.parse(heartbeat) > Date.parse(new Date()) - 600000)) { //10min
        return marker_base + "marker_yellow.png";
    } else { // not triggered && lost heartbeat for over 10min
        return marker_base + "marker_grey.png";
    }
}

function changeMarkerStatus(sensor) {
    marker_base = "/static/images/markers/";

    // var x = Math.floor(Math.random() * 3);
    // var marker = [marker_base + "marker_red.png",marker_base + "marker_yellow.png",marker_base + "marker_green.png"]
    // console.log(marker[x])
    // return marker[x]

    current_state = sensor['state']
    last_updated = sensor['updated_at']
    last_triggered = sensor['last_triggered']
    last_notified = sensor['last_notified']
    last_heartbeat = sensor['last_heartbeat']

    if ((current_state == 'Trigger') && ((Date.parse(last_triggered) + 300000 ) > Date.parse(new Date()))) { //
        return marker_base + "marker_yellow.png";
    } else if ((current_state == 'Processing') && ((Date.parse(last_triggered) + 300000 ) > Date.parse(new Date()))) {
        return marker_base + "marker_red.png";
    } else if ((current_state == 'PostProcessing') && ((Date.parse(last_notified) + 300000 ) > Date.parse(new Date()))) {
        return marker_base + "marker_red.png";
    }else if ((current_state == 'Steady') && ((Date.parse(last_updated) + 300000 ) > Date.parse(new Date()))) {
        return marker_base + "marker_green.png";
    }
    else if ((Date.parse(last_updated) + 600000 ) > Date.parse(new Date())) {
        return marker_base + "marker_green.png";
    }else{
        return marker_base + "marker_grey.png";
    }


    // if (triggered && (Date.parse(triggered) > Date.parse(new Date()) - 30000)) { // 30sec
    //     return marker_base + "marker_red.png";
    // } else if (heartbeat && (Date.parse(heartbeat) > Date.parse(new Date()) - 120000)) { //2min
    //     return marker_base + "marker_green.png";
    // } else if (heartbeat && (Date.parse(heartbeat) > Date.parse(new Date()) - 600000)) { //10min
    //     return marker_base + "marker_yellow.png";
    // } else { // not triggered && lost heartbeat for over 10min
    //     return marker_base + "marker_grey.png";
    // }
}


function modal(sensor) {
    //isBase = false;
    var info = null;
    // modal background
    var bg = $("<div id=modal-background>")
        .css({
            position: "fixed",
            display: "block",
            zIndex: "9999",
            left: "0px",
            top: "0px",
            width: "100%",
            height: "100%",
            overflow: "auto",
            backdropFilter: "blur(3px)",
            backgroundColor: "rgba(0,0,0,0.4)",
        })
        .appendTo("body");

    var cell = document.getElementById("details");
    while (cell.hasChildNodes()) {
        cell.removeChild(cell.firstChild);
    }

    //modal box
    var modalContent = $("#details")
        .append(
            '<div id="info" style="width: 100%; margin-top: 5%">' +
            '<h4 style="margin-top: 1%">센서 정보</h4>' +
            '<button style="position: absolute; top: 7.6%; right: 2.5%" id="edit-button" type="button" class="btn btn-secondary" style="float: right; font-size: 16px">수정</button>' +
            '<div id="sensor-info"></div>' +
            '<br/>'
            // '<h4 class="sensor-install-info">센서 설치 장소</h4>' +
            // '<div id="sensor-install" class="sensor-install-info" style="display: flex; overflow-x: auto; height: 200px"></div>'
            // '<form id="uploadForm" enctype="multipart/form-data">' +
            // '<div style="display: flex; justify-content: center; align-items: center; float: right"></div>' +
            // '<label class="btn btn-secondary btn-block" style="width: 12%" float: right>사진추가' +
            // '<input type="file" name="_method" value="PUT" id= "imageInput" style="display: none;" accept="image/*" /></label>' +
            // '<input class="btn btn-secondary btn-block" style="width: 10%" float: right; id="btnSubmit" type="submit">' +
            // '<img style="width: 50px; height: 50px" id="preview" src="#" alt="preview image" /></form>'
        )
        .append(
            '<span class="close" style="cursor:pointer; width: fit-content; height: fit-content; position: fixed; right: 2%">&times;</span>'
        );

    sensor_info = $("#sensor-info")
        .css({
            width: "100%",
        })
        .append('<table id="sensor-table"></table>');
    table = $("#sensor-table").attr("class", "table");

    /**
     * @deprecated stat-table may be deprecated
     */
    table = $("#stat-table").attr("class", "table");
    table.css({
        width: "100%",
    });

    modalContent.css({
        position: "fixed",
        display: "flex",
        overflowY: "auto",
        borderRadius: "10px",
        backgroundColor: "rgb(255, 255, 255)",
        zIndex: "10000",
        margin: "auto",
        padding: "20px",
        border: "1px solid #888",
        width: "50%",
        height: "85%",
        minWidth: "800px",
        minHeight: "800px",
        top: "50%",
        left: "50%",
        float: "left",
        transform: "translate(-50%, -50%)",
        msTransform: "translate(-50%, -50%)",
        webkitTransform: "translate(-50%, -50%)",
    });
    modalContent.appendTo("body");

    const imgInp = document.getElementById('imageInput');
    const _prev = document.getElementById('preview');
    const btnSubmit = document.getElementById('btnSubmit');
    // const uploadForm = document.getElementById('uploadForm');



    // uploadForm.action = `/api/sensor/images?sensor_id=${sensor.uuid}`;
    // uploadForm.method = "POST";
    // $('#uploadForm').on('submit', function (e) {
    //     var frm = $(this)
    //     e.preventDefault()
    //     $.ajax({
    //         type: frm.attr('method'),
    //         url: frm.attr('action'),
    //         data: frm.serialize(),
    //         success: function (data) {
    //         }
    //     });
    // })
    // $(function () {
    //     var frm = $("#uploadForm");
    //     frm.submit(function (ev) {
    //         $.ajax({
    //             type: frm.attr('method'),
    //             url: frm.attr('action'),
    //             data: frm.serialize(),
    //             success: function(data) {
    //                 alert('ok')
    //             }
    //         });
    //         ev.preventDefault()
    //     })
    // })
    // imgInp.onchange = e => {
    //     const [file] = imgInp.files;
    //     if (file) {
    //         _prev.src = URL.createObjectURL(file);
    //     }
    // }

    document
        .getElementsByClassName("close")[0]
        .addEventListener("click", function () {
            bg.remove();
            modalContent.hide();
        });
}

function setMapOnAll(map) {
  for (let i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  }
}

function setMarker(sensor) {
    var sensor_num, sensor_status;
    var markers = [];
    for (var i = 0; i < sensor.length; i++) {
        sensor_num = sensor[i];
        sensor_status = changeMarkerStatus(sensor_num);

        latlng = new naver.maps.LatLng(
            sensor_num.location.coordinates[1],
            sensor_num.location.coordinates[0]
        );
        marker = new naver.maps.Marker({
            position: latlng,
            map: map,
            icon: {
                url: sensor_status,
            },
        });
        markers.push(marker);
    }

    function getClickHandler(seq) {
        return function (e) {
            modal(sensor[seq]);
            //sensor-info
            fetch(`/api/sensor-info?sensor_id=${sensor[seq].uuid}`)
                .then((res) => res.json())
                .then((res) => makeTable("sensor-table", res));
            loadImages(sensor[seq].uuid);
        };
    }

    for (var i = 0; i < markers.length; i++) {
        naver.maps.Event.addListener(markers[i], "click", getClickHandler(i));
    }
    /*      set cluster     */
    var htmlMarker1 = {
            content:
                '<div style="cursor:pointer;width:40px;height:40px;line-height:42px;font-size:10px;color:white;text-align:center;font-weight:bold;background:url(../static/images/cluster/cluster-marker-1.png);background-size:contain;"></div>',
            size: N.Size(40, 40),
            anchor: N.Point(20, 20),
        },
        htmlMarker2 = {
            content:
                '<div style="cursor:pointer;width:40px;height:40px;line-height:42px;font-size:10px;color:white;text-align:center;font-weight:bold;background:url(../static/images/cluster/cluster-marker-2.png);background-size:contain;"></div>',
            size: N.Size(40, 40),
            anchor: N.Point(20, 20),
        },
        htmlMarker3 = {
            content:
                '<div style="cursor:pointer;width:40px;height:40px;line-height:42px;font-size:10px;color:white;text-align:center;font-weight:bold;background:url(../static/images/cluster/cluster-marker-3.png);background-size:contain;"></div>',
            size: N.Size(40, 40),
            anchor: N.Point(20, 20),
        },
        htmlMarker4 = {
            content:
                '<div style="cursor:pointer;width:40px;height:40px;line-height:42px;font-size:10px;color:white;text-align:center;font-weight:bold;background:url(../static/images/cluster/cluster-marker-4.png);background-size:contain;"></div>',
            size: N.Size(40, 40),
            anchor: N.Point(20, 20),
        },
        htmlMarker5 = {
            content:
                '<div style="cursor:pointer;width:40px;height:40px;line-height:42px;font-size:10px;color:white;text-align:center;font-weight:bold;background:url(../static/cluster/cluster-marker-5.png);background-size:contain;"></div>',
            size: N.Size(40, 40),
            anchor: N.Point(20, 20),
        };

    var markerClustering = new MarkerClustering({
        minClusterSize: 2,
        maxZoom: 13,
        map: map,
        markers: markers,
        disableClickZoom: false,
        gridSize: 120,
        icons: [
            htmlMarker1,
            htmlMarker2,
            htmlMarker3,
            htmlMarker4,
            htmlMarker5,
        ],
        indexGenerator: [10, 100, 200, 500, 1000],
        stylingFunction: function (clusterMarker, count) {
            $(clusterMarker.getElement()).find("div:first-child").text(count);
        },
    });

    return markers

}

/**
 * make table using data except for exception
 *
 * @param {string} id id of table
 * @param {Object} data set of {key, value}
 * @param {Array} exception exception key for representing on table
 */
function makeTable(id, data, exception = []) {
    const table = $("#" + id);
    table.empty();

    let translate_key = {
        location: "위치[경도,위도]",
        address: "주소",
        site_name: "설치 국소",
        name: "센서 이름",
        sensor_id: "센서 ID",
        last_triggered: "최근 트리거 발생 일시",
        last_heartbeat: "최근 상태 정보 일시",
        last_notified: "최근 알림 일시",
        description: "설명"
    };
    let translate_sensor_status = {
        normal: "정상",
        offline: "전원 꺼짐",
        event_happened: "이벤트 발생",
    };
    const noData = "데이터 없음";

    // for (const key in data) {
    for (const key in translate_key) {
        if (exception.includes(key)) {
            continue;
        }

        let tr = table.append("<tr></tr>");
        if (translate_key[key]) {
            tr.append("<th>" + translate_key[key] + "</th>");
        } else {
            continue;
        }

        if (key == "location") {
            tr.append(
                `<td style="display: flex; flex-direction: row" >
                    <input 
                        type="text" 
                        id="${key}" 
                        value="[${data["longitude"].toString().slice(0, 7)}, ${data["latitude"].toString().slice(0, 6)}]" 
                        style="width: 100%; border: none"
                    />
                </td>`
            );
        } else if (key == "address") {
            tr.append(`<td>
            <input 
                type="text" 
                id="${key}" 
                value="${data["address"] || noData}" 
                style="width: 100%; border: none"
            />
        </td>`);
        } else if (key == "site_name") {
            tr.append(`<td>
            <input 
                type="text" 
                id="${key}" 
                value="${data["site_name"]}" 
                style="width: 100%; border: none"
            />
        </td>`);
        } else if (key == "description") {
            tr.append(`<td>
            <input 
                type="text" 
                id="${key}" 
                value="${data["description"]}" 
                style="width: 100%; border: none"
            />
        </td>`);
        } else if (
            key == "last_triggered" ||
            key == "last_heartbeat" ||
            key == "last_notified"
        ) {
            if (data[key] == null) {
                tr.append("<td>데이터 없음</td>");
            } else {
                tr.append("<td>" + data[key] + "</td");
            }
        } else {
            if (data[key] == null) {
                tr.append(
                    '<td><input type="text" id = ' +
                    key +
                    ' value="데이터 없음" style="width: 100%; border: none"/></td>'
                );
            } else {
                tr.append(
                    '<td> <input type="text" id = ' +
                    key +
                    ' value="' +
                    data[key] +
                    '" style="width: 100%; border: none"/></td>'
                );
            }
        }
    }
    document.getElementById("edit-button").onclick = function () {
        // const address1 = document.getElementById("address").value;
        // const description1 = document.getElementById("description").value;
        // const name2 = document.getElementById("name").value;

        // const address1 = (address1 || noData)
        // const description1 = document.getElementById("description");
        // const name2 = document.getElementById("name");
        // console.log(address1);

        let params = {
            address: document.getElementById("address").value,
            description: document.getElementById("description").value,
            name: document.getElementById("name").value,
        };

        $.ajax({
            url: `/api/sensor-info?sensor_id=${data.sensor_id}`,
            type: "PUT",
            data: JSON.stringify(params),
            contentType: "application/json",
            success: function (res) {
                location.reload(true);
            },
            error: function () {
                console.err("generateReport: ajax: error");
            },
        });
    };
}

function loadImages(uuid) {
    const imgDOM = document.getElementById('sensor-install');
    fetch(`/api/sensor/images?sensor_id=${uuid}`)
        .then(res => res.json())
        .then(res => res.imgs.map((img, i) => {
            // console.log(imgd.location);
            insertImage(img.location, imgDOM, i);
        }));
}

function insertImage(location, imgDOM, i) {
    let curImg = document.createElement('img');
    fetch(`/api/images?location=${location}`)
        .then(res => curImg.setAttribute('src', res.url));
    curImg.setAttribute('id', `sensor_img${i}`);
    imgDOM.appendChild(curImg);
}