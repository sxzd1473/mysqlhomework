document.addEventListener('DOMContentLoaded', function () {
    // 点击添加对局按钮弹出模态框并填充当前时间
    document.getElementById('addMatchBtn').addEventListener('click', function () {
        const currentDate = new Date();

        const year = currentDate.getFullYear();
        const month = currentDate.getMonth() + 1; // 月份是从0开始的，所以要加1
        const day = currentDate.getDate();

        const hours = currentDate.getHours();
        const minutes = currentDate.getMinutes();
        const seconds = currentDate.getSeconds();
        console.log(currentDate);
        document.getElementById('match_time').value = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    });


    document.getElementById('submitMatchForm').addEventListener('click', function () {
        var formData = new FormData(document.getElementById('matchForm'));
        var data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        fetch('/matches/add/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(response => response.json())
            .then(() => {
                document.getElementById('addMatchModal').style.display = 'none';
                location.reload();
            })
            .catch(error => console.error('Error:', error));
    });



    // 点击添加对局按钮弹出模态框并填充当前时间
    var edbuttons = document.querySelectorAll('button[id^="editMatchBtn_"]');
    var EditingMatchId = null;

    edbuttons.forEach(function (button) {
        button.addEventListener('click', function () {

            // 获取数据属性
            EditingMatchId = this.getAttribute('data-id'); // 如果需要，可以替换为具体数据
            const matchMode = this.getAttribute('data-mode');
            const matchTime = this.getAttribute('data-time');
            const matchDuration = this.getAttribute('data-duration');
            const matchResult = this.getAttribute('data-result');
            const matchMap = this.getAttribute('data-map');

// 将数据填充到编辑表单
            document.getElementById('edit_match_mode').value = matchMode;        // 填充比赛模式
            document.getElementById('edit_match_time').value = matchTime;        // 填充比赛时间
            document.getElementById('edit_match_duration').value = matchDuration; // 填充比赛时长
            document.getElementById('edit_match_result').value = matchResult;    // 填充比赛结果
            document.getElementById('edit_match_map').value = matchMap;          // 填充比赛地图

        });
    });
    document.getElementById("submitEditMatchForm").addEventListener('click', function () {
        var formData = new FormData(document.getElementById('editMatchForm'));
        var data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });
        fetch('/matches/edit/' + EditingMatchId + '/', {
            url: '/matches/edit/' + EditingMatchId + '/',
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }).then(response => response.json())
            .then(() => {
                document.getElementById('editMatchModal').style.display = 'none';
                location.reload();
            });
        EditingMatchId = null;

    });
    //计数
    document.getElementById("allMatchCountBtn").addEventListener("click", function allMatchCount() {
        var edbuttons = document.querySelectorAll('button[id^="editMatchBtn_"]');
        document.getElementById('allMatchCountOutput').innerHTML = "总计存储了" + edbuttons.length+'个对局';
    })


});

// 删除对局的函数
function deleteMatch(matchId) {
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


