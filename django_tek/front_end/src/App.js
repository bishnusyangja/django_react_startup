import React, {useState} from 'react';
import logo from './logo.svg';
import './App.css';



const getCookie = (name) => {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
    else return null;
}

let params = {credentials: 'same-origin', method: 'POST', headers : {
                "X-CSRFToken": getCookie("csrftoken"),
                "Accept": "application/json",
                "Content-Type": "application/json"
                },
//                body: JSON.stringify(data)
            }


function post_request(url, data){
    let p_data = params;
    p_data['body'] = JSON.stringify(data);
    fetch(url, params).then(function(response){
        if (!response.ok){
            return response.json().then(json => {throw json});
        }
        return response.json()
    }).then((json) => {
        console.log(json);
//        that.props.onHide();
//        that.props.add_attachment(json);
    }).catch(function(err){
//        that.props.update_errors(err);
        console.log(err);
    });

}



function App() {
    let margin_style = {margin: '20px'}
    let display_style = {display: 'block'};

    const [login_name, set_login_name] = useState('');
    const [login_password, set_login_password] = useState('');

    const [register_first_name, set_register_first_name] = useState('');
    const [register_last_name, set_register_last_name] = useState('');
    const [register_email, set_register_email] = useState('');
    const [register_username, set_register_username] = useState('');

    const handleChangeLoginName = event => set_login_name(event.target.value);
    const handleChangeLoginPassword = event => set_login_password(event.target.value);

    const handleChangeRegisterFirstName = event => set_register_first_name(event.target.value);
    const handleChangeRegisterLastName = event => set_register_last_name(event.target.value);
    const handleChangeRegisterEmail = event => set_register_email(event.target.value);
    const handleChangeRegisterUserName = event => set_register_username(event.target.value);



    const submitRegister = event => {
        event.preventDefault();
        let url = '/user/';
        let data = {first_name: register_first_name, last_name: register_last_name,
                        email: register_email, username: register_username};
        console.log(data);
        let params = {credentials: 'same-origin', method: 'POST', headers : {
                "X-CSRFToken": getCookie("csrftoken"),
                "Accept": "application/json",
                "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            }
        post_request(url, data);
    }

    const submitLogin = event => {
        event.preventDefault();
        let url = '/api-login/';
        let data = {username: login_name, password: login_password};
        let params = {credentials: 'same-origin', method: 'POST', headers : {
                "X-CSRFToken": getCookie("csrftoken"),
                "Accept": "application/json",
                "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            }
        post_request(url, data);
    }


  return (
    <div className="App">
      <div> Welcome to Tekkon App </div>

      <div style={margin_style}>
          <form id="login-form" onSubmit={submitLogin}>
              <input type="text" placeholder="Username" style={display_style} onChange={handleChangeLoginName}/>
              <input type="password" placeholder="Password" style={display_style} onChange={handleChangeLoginPassword}/>

              <button type="submit" style={display_style}> Login</button>
          </form>
      </div>

      <div style={margin_style}>
          <form id="registration-form" onSubmit={submitRegister}>
              <input type="text" placeholder="First Name"  onChange={handleChangeRegisterFirstName} style={display_style}/>
              <input type="text" placeholder="Last Name" onChange={handleChangeRegisterLastName} style={display_style}/>
              <input type="text" placeholder="Email" onChange={handleChangeRegisterEmail} style={display_style}/>
              <input type="text" placeholder="Username" onChange={handleChangeRegisterUserName} style={display_style}/>

              <button type="submit" style={display_style}>Sign Up</button>
          </form>
      </div>

      <div style={margin_style}>
          <form id="forgot-password-form">
              <input type="text" placeholder="Email" style={display_style}/>
              <button type="submit" style={display_style}>Forgot Password</button>
          </form>
      </div>

      <div style={margin_style}>
          <form id="login-with-facebook-form">
              <button type="submit" style={display_style}> Login With Facebook </button>
          </form>
      </div>
    </div>
  );
}

export default App;
