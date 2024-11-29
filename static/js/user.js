document.addEventListener("DOMContentLoaded", function () {
    var playerId = document.getElementById('player-info').dataset.playerId;
    var global_data = {};
    fetch(`/playerRecords/?player_id=${playerId}`)
    .then(response => response.json())
            .then(data => {
                global_data = data;
                // 清空现有的表格数据
                var tableBody = document.querySelector('tbody');
                if (data['results'].length == 0) {
                    tableBody.innerHTML = '<tr><td colspan="8">最近还未进行比赛</td></tr>';
                    return;
                }
                tableBody.innerHTML = '';
                console.log(data);
                // 根据返回的数据填充表格
                data['results'].forEach(record => {
                    var row = `<tr>
                        <td>${record.pmatchId}</td>
                        <td>${record.playerId}</td>
                        <td>${record.matchId}</td>
                        <td>${record.killCount}</td>
                        <td>${record.kd}</td>
                        <td>${record.deathCount}</td>
                        <td>${record.rankpoints}</td>
                        <td><button class="btn-primary btn-sm disabled" id="deleteKillRecordBtn_{{ loop.index }}">
                            查看
                        </button></td>
                        </tr>`;
                    tableBody.innerHTML += row;
                });
            })
    var match_num = global_data['results'].length;
    $('#match_num').innerHTML = "最近比赛数："+match_num;
})