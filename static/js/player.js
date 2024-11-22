document.getElementById('submitPlayerForm').addEventListener('click', function () {
    var formData = new FormData(document.getElementById('playerForm'));
    var data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    fetch('/players/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(() => {
            document.getElementById('addPlayerModal').modal('hide');
            location.reload();
        })
        .catch(error => console.error('Error:', error));
});
//修改与删除
document.getElementById('submitEditPlayerForm').addEventListener('click', function () {
    var formData = new FormData(document.getElementById('editPlayerForm'));
    var data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });
    var data_id = document.getElementById('editPlayerForm').getAttribute('data_id');
    const editButtons = document.querySelectorAll('#editPlayerBtn');
    const playerId = this.getAttribute('data-id');
            const playerName = this.getAttribute('data-name');
            const playerRank = this.getAttribute('data-rank');
            const playerKda = this.getAttribute('data-kda');

            // 将数据填充到编辑表单
            document.getElementById('edit_player_id').value = playerId;
            document.getElementById('edit_player_name').value = playerName;
            document.getElementById('edit_player_rank').value = playerRank;
            document.getElementById('edit_player_kda').value = playerKda;

fetch('/players/edit/' + data_id, {
    method: 'PUT',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
}).then(response => response.json())
    .then(() => {
        document.getElementById('editPlayerModal').modal('hide');
        location.reload();
    })
    .catch(error => console.error('Error:', error));

});


// 删除玩家的函数
function deletePlayer(playerId) {
    if (confirm('确定要删除这个玩家吗？')) {
        console.log('删除玩家：' + playerId);
        fetch('/players/delete/' + playerId, {
            url: '/players/delete/' + playerId,
            method: 'DELETE',
            success: function (result) {
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
            })
            .catch(error => console.error('Error:', error));
        ;
    }
}
