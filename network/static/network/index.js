function edit_post(post_id) {
    document.querySelector(`#post_text_${post_id}`).innerHTML = '';
    const text = document.querySelector(`#original_text_${post_id}`).innerHTML;
    document.querySelector(`#original_text_${post_id}`).style.display = 'none';
    document.querySelector(`#post_text_${post_id}`).style.display = 'block';

    document.getElementById(`post_text_${post_id}`).innerHTML = `<textarea rows="3" cols="90" id="new_text_${post_id}">${text}</textarea><br><button id="save_${post_id}" class="btn-top">Save</button>`;

    document.querySelector(`#save_${post_id}`).onclick = () => {
      fetch(`/posts/${post_id}`, {
          method: 'POST',
          body: JSON.stringify({
            text: document.querySelector(`#new_text_${post_id}`).value
          })
      })
      .then(response => response.json())
      .then(result => {
          if ("message" in result) {
            document.querySelector(`#original_text_${post_id}`).innerHTML = document.querySelector(`#new_text_${post_id}`).value;
            document.querySelector(`#original_text_${post_id}`).style.display = 'block';
            document.querySelector(`#post_text_${post_id}`).style.display = 'none';
            location.reload();
            }
          else {
            alert(result.error)
          }
      })

    }
    return false;
}

function like_post(post_id) {
  fetch('/likes', {
      method: 'POST',
      body: JSON.stringify({
        post_id: post_id
      })
  })
  .then(response => response.json())
  .then(result => {
      if ("message" in result) {
        location.reload();
        console.log(result.message)
      }
      else {
        alert(result.error)
      }
    });
}

function unlike_post(post_id) {
  fetch('/unlike', {
      method: 'POST',
      body: JSON.stringify({
        post_id: post_id
      })
  })
  .then(response => response.json())
  .then(result => {
      if ("message" in result) {
        location.reload();
        console.log(result.message)
      }
      else {
        alert(result.error)
      }
    });
}
