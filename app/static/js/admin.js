
function updateRole(role, userId) {
    fetch('/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            role: role,
            id: userId
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to update role');
        }
        return response.json();
    })
    .then(data => {
        console.log('Role updated successfully:', data);
        let userRow = document.getElementById('role_column_' + userId);
        userRow.innerText ="";

        let updatedRole = role;
        console.log(updatedRole);
      
        if (updatedRole === '1') {
            let userRow = document.getElementById('role_column_' + userId);
            userRow.innerHTML = ""; // 기존 내용 삭제

            // 삭제 버튼 생성 및 추가
            let deleteButton = document.createElement("button");
            deleteButton.textContent = "DELETE";
            deleteButton.onclick = function() {
                deleteUser(userId);
            };
            userRow.appendChild(deleteButton);
            
        } else {
            // 사용자 역할이 1이 아닌 경우 버튼 제거
            let userRow = document.getElementById('role_column_' + userId);
            userRow.innerHTML = "";
        }
    })
    .catch(error => {
        console.error('Error updating role:', error);
    });
}

function deleteUser(userId) {
    if (confirm("really want to delete?")) {
        fetch('/delete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id: userId
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to delete user');
            }
            return response.json();
        })
        .then(data => {
            console.log('User deleted successfully:', data);
            let userRow = document.getElementById('user_row_' + userId);
            if (userRow) {
                userRow.parentNode.removeChild(userRow);
            }
           
        })
        .catch(error => {
            console.error('Error deleting user:', error);
        });
    }
}