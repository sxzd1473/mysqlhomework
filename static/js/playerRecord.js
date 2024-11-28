document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('kill_count').addEventListener('input', updateKD);
    document.getElementById('death_count').addEventListener('input', updateKD);
    function updateKD() {
        var killCount = parseFloat(document.getElementById('kill_count').value) || 0;
        var deathCount = parseFloat(document.getElementById('death_count').value) || 1; // 避免除以0
        // 计算 KD 值，并保留两位小数
        var kdValue = (killCount / deathCount);
        document.getElementById('kd').value = kdValue.toFixed(2);
        document.getElementById('rankpoints').value = (killCount * 3)-deathCount*2;
    }
    document.getElementById('PlayerRecordFormBtn').addEventListener('click', function () {
        var formData = new FormData(document.getElementById('PlayerRecordForm'));
        var data = {};
        formData.forEach((value, key) => {
            if(value == '' || value == null) {alert('请填写所有必填项'); return false;}
            data[key] = value;
        });
        document.getElementById('kd').value = (data['killCount'] / data['deathCount']).toFixed(2);
        fetch('/playerRecords/add/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(response => response.json())
            .then(() => {
                document.getElementById('addPlayerRecordModal').style.display = 'none';
                location.reload();
            })
    });
    document.getElementById('searchBtn').addEventListener('click', function () {
        var matchId = document.getElementById('searchMatchId').value;
        fetch(`/playerRecords/?match_id=${matchId}`)
            .then(response => response.json())
            .then(data => {
                if (data['results'].length == 0) {
                    var tableBody = document.querySelector('tbody');
                    tableBody.innerHTML = '<tr><td colspan="8">没有找到相关记录</td></tr>';
                    return;
                }
                console.log(data);
                // 清空现有的表格数据
                var tableBody = document.querySelector('tbody');
                tableBody.innerHTML = '';
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
                        <td><button class="btn btn-danger btn-sm disabled">删除</button></td>
                        </tr>`;
                    tableBody.innerHTML += row;
                });
            })
    });
    document.getElementById('delKillRecordBtn').addEventListener('click', function () {
        var matchId = document.getElementById('delMatchId').value;
        fetch(`/playerRecords/delete/?match_id=${matchId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(response => response.json())
            .then(() => {
                location.reload();
            });
    });
    document.getElementById('searchPlayerBtn').addEventListener('click', function () {
        var playerId = document.getElementById('searchPlayerId').value;
        fetch(`/playerRecords/?player_id=${playerId}`)
            .then(response => response.json())
            .then(data => {
                if (data['results'].length == 0) {
                    var tableBody = document.querySelector('tbody');
                    tableBody.innerHTML = '<tr><td colspan="8">没有找到相关记录</td></tr>';
                    return;
                }
                // 清空现有的表格数据
                var tableBody = document.querySelector('tbody');
                tableBody.innerHTML = '';
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
                        <td><button class="btn btn-danger btn-sm disabled">删除</button></td>
                        </tr>`;
                    tableBody.innerHTML += row;
                });
            })
    });
    document.getElementById('delPlayerRecordBtn').addEventListener('click', function () {
        var playerId = document.getElementById('delPlayerId').value;
        fetch(`/playerRecords/delete/?player_id=${playerId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(response => response.json())
            .then(() => {
                location.reload();
            });
    });
    document.getElementById("allRecordCountBtn").addEventListener("click", function allRecordCount() {
        var num_of_trs = document.querySelectorAll('tbody tr').length;
        document.getElementById('allRecordCountOutput').innerHTML = "总计存储了" + num_of_trs+'条记录';
    })
});

// 外键
$(document).ready(function () {
    // 查询比赛ID
    $.ajax({
        url: '/matches/', // 替换为你的 API 路径
        method: 'GET',
        success: function (data) {
            // 假设 data 是一个包含 matchId 的数组
            var matchSelect = $('#match_id');
            matchSelect.empty(); // 清空选择框
            matchSelect.append('<option value="">请选择比赛ID</option>');
            for (var i = 0; i < data['results'].length; i++) {
                matchSelect.append('<option value="' + data['results'][i].id + '">' + data['results'][i].id + '</option>');
            }
        },
        error: function (err) {
            console.error('获取比赛ID失败:', err);
        }
    });

    // 查询玩家ID
    $.ajax({
        url: '/players/', // 替换为你的 API 路径
        method: 'GET',
        success: function (data) {
            // 假设 data 是一个包含 playerId 的数组
            var playerSelect = $('#player_id');
            playerSelect.empty(); // 清空选择框
            playerSelect.append('<option value="">请选择玩家ID</option>');
            for (var i = 0; i < data['results'].length; i++) {
                playerSelect.append('<option value="' + data['results'][i].id + '">' + data['results'][i].id + '</option>');
            }
        },
        error: function (err) {
            console.error('获取玩家ID失败:', err);
        }
    });
});


