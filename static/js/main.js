function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const like = () => {
    const question = document.querySelectorAll('.voting')

    for(const item of question) {
        const likeButton = item.querySelector('.like-button')
        const likeCounter = item.querySelector('.vote-count')

        likeButton.addEventListener('click', () => {
            const request = new Request(`/like_async/${likeButton.dataset.objectid}/${likeButton.dataset.objecttype}`, {
                method: 'post',
                headers: {
                    'Content-Type':'application/json',
                    'X-CSRFToken' : getCookie('csrftoken')
                }
            })

            fetch(request)
                .then((response) => response.json())
                .then((data) => likeCounter.innerHTML = data.likes_count) 

        })
    }
}

const correct = () => {
    const answer = document.querySelectorAll('.form-check')
    for(const item of answer) {
        const checkBox = item.querySelector('.correct-check')
        const answer_id = checkBox.dataset.answerid;

        checkBox.addEventListener('click', () => {
            const request = new Request(`correct_change/${answer_id}/${checkBox.dataset.questionid}`, {
                method: 'post',
                headers: {
                    'Content-Type':'application/json',
                    'X-CSRFToken' : getCookie('csrftoken')
                }
            })
            fetch(request)
                .then((response) => response.json())
            for(const ans of answer)
                {
                    const cb = ans.querySelector('.correct-check')
                    if(cb.dataset.answerid != answer_id)
                        cb.checked = false

                }
        })
    }
        
}

like()
correct()