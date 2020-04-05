# Discord self-bot scripts

Discord claims to care about privacy but they don't really, just read their vague Privacy Policy.
It's also my opinion that they don't have a sustainable business model, so when the VC money runs out and time comes to monetize, I don't find it unreasonable that they would resort to selling user data.
That's why I don't trust them with my message history, so I erase it regularly.
There is also the risk of account theft, doxing, and so on. I also don't want to come back in 15 years to read cringe.
Thus I firmly believe message history should be ephemeral.

These scripts are for self-botting; the auth token is NOT a bot API key; you need to extract this from your client.
It's a clear ToS violation so I claim no responsibility if you get banned for using these. Use at your own risk and discretion!

### Self-delete Javascript-let

Check out this Gist for a script you can run in your client's Javascript console (aka "inspect element").
https://gist.github.com/rcx/a29eac843a8ecf97a22accb34ef60b88

### Grabbing auth token

Just paste this into your web developer tools JS console. Works in electron client, Chrome, and Firefox

```javascript
authToken = "";
function grabAuthToken() {
    if (authToken.length === 0) {
        // Lmao bypass token security measures
        window.onbeforeunload = grabAuthToken;
        window.location.reload();

        // yoink
        var localToken = document.body.appendChild(document.createElement(`iframe`)).contentWindow.localStorage.token;
        if (localToken !== undefined) {
            authToken = JSON.parse(localToken);
            window.alert("Your token is " + authToken);
        }
    }
    return false;
}
window.alert("Grabbing your auth token. If a confirm window shows up, please click 'Cancel' in Chrome / 'Stay on Page' in Firefox.");
grabAuthToken()
```

# License

MIT License
