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
            $('#addPlayerModal').modal('hide');
            location.reload();
        })
        .catch(error => console.error('Error:', error));
});
//修改与删除
$('#editPlayerModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var id = button.data('id');
    var name = button.data('name');
    var rank = button.data('rank');
    var kda = button.data('kda');

    var modal = $(this);
    modal.find('#edit_player_id').val(id);
    modal.find('#edit_player_name').val(name);
    modal.find('#edit_player_rank').val(rank);
    modal.find('#edit_player_kda').val(kda);
});

// 提交编辑表单
$('#submitEditPlayerForm').on('click', function () {
    $('#editPlayerForm').submit();
});

// 删除玩家的函数
function deletePlayer(playerId) {
    if (confirm('确定要删除这个玩家吗？')) {
        $.ajax({
            url: '/players/' + playerId,
            type: 'DELETE',
            success: function (result) {
                // 在页面上刷新数据
                location.reload();
            },
            error: function (err) {
                alert('删除失败: ' + err.responseText);
            }
        });
    }
}
