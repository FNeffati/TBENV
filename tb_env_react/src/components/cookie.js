import React, { useState } from 'react';

function Cookie() {

  const [message, setMessage] = useState('');

  const fetchData = () => {
      fetch("/hello",
          {
              method: "GET",
              headers: {
                  "Content-Type": "applications/json",
              },
          })
          .then((response) => response.json())
          .then((data) => {
              setMessage(data.message)
          })
          .catch((error) => {
              console.error("ERROR HAPPENED", error)
          })
  }

  return (
    <div>
        <p>
            This is from the component.
        </p>
      <h1>{message}</h1>
      <button onClick={fetchData}>Fetch Data</button>
    </div>
  )
}


export default Cookie;