document.addEventListener('DOMContentLoaded', function () {

    document.getElementById('submitKillRecordForm').addEventListener('click', function () {
        var formData = new FormData(document.getElementById('killRecordForm'));
        var data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });
        console.log(data);
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


});

// 删除对局的函数
function deleteKillRecord(matchId) {
    if (confirm('确定要删除这个对局吗？')) {
        console.log('删除对局：' + matchId);
        fetch('/matches/delete/' + matchId + '/', {
            url: '/matches/delete/' + matchId + '/',
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            success: function () {
                // 在页面上刷新数据
                location.reload();
            },
            error: function (err) {
                alert('删除失败: ' + err.responseText);
                location.reload();
            }
        })
            .then(response => response.json())
            .then(() => {
                location.reload();
            });
    }
}

function deleteExpiredMatch() {
    if (confirm('确定要删除所有过期对局吗？')) {

        fetch('/matches/delete/', {
            url: '/matches/delete/',
            method: 'DELETE',
            success: function () {
                // 在页面上刷新数据
                location.reload();
            },
            error: function (err) {
                alert('删除失败: ' + err.responseText);
                location.reload();
            }
        })
            .then(response => response.json())
            .then(() => {
                location.reload();
            });
    }
}


// 使用 jQuery 发送 AJAX 请求
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


