document.addEventListener('DOMContentLoaded', function () {

    document.getElementById('submitKillRecordForm').addEventListener('click', function () {
        var formData = new FormData(document.getElementById('killRecordForm'));
        var data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });
        fetch('/matchRecords/add/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(response => response.json())
            .then(() => {
                document.getElementById('addKillRecordModal').style.display = 'none';
                location.reload();
            })
            .catch(error => console.error('Error:', error));
    });
    document.getElementById('searchBtn').addEventListener('click', function () {
        var matchId = document.getElementById('searchMatchId').value;
        fetch('/matchRecords/' + matchId)
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
                            <td>${record.recordId}</td>
                            <td>${record.matchId}</td>
                            <td>${record.killerId}</td>
                            <td>${record.victimId}</td>
                            <td>${record.killTime}</td>
                            <td>${record.meansOfDeath}</td>
                            <td>${record.coordinates}</td>
                            <td><button class="btn btn-danger btn-sm disabled">删除</button></td>
                        </tr>`;
                    tableBody.innerHTML += row;
                });
            })
    })
    document.getElementById('delKillRecordBtn').addEventListener('click', function () {
        var matchId = document.getElementById('delMatchId').value;
        fetch('/matchRecords/delete/' + matchId + '/', {
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
            var killerSelect = $('#killer_id');
            var victimSelect = $('#victim_id');
            killerSelect.empty(); // 清空选择框
            victimSelect.empty();
            killerSelect.append('<option value="">请选择击杀者ID</option>');
            victimSelect.append('<option value="">请选择受害者ID</option>');
            for (var i = 0; i < data['results'].length; i++) {
                killerSelect.append('<option value="' + data['results'][i].id + '">' + data['results'][i].id + '</option>');
                victimSelect.append('<option value="' + data['results'][i].id + '">' + data['results'][i].id + '</option>');
            }
        },
        error: function (err) {
            console.error('获取玩家ID失败:', err);
        }
    });
});


function deleteByMatch(matchId) {
    if (confirm('确定要删除这个对局吗？')) {
        console.log('删除对局：' + matchId);
        fetch('/matches/delete/' + matchId + '/', {
            url: '/matches/delete/' + matchId + '/',
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(() => {
                location.reload();
            });
    }
}

