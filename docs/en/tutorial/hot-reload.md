# Hot Reload

FastUI supports automatic browser refresh when source files change during development.

## Enabling Hot Reload

```python
if __name__ == "__main__":
    app.run(hot_reload=True)
```

## How It Works

When `hot_reload=True` is set:

1. **File watcher**: A background thread polls `.py` files using `os.stat()` every second
2. **Polling scope**: All `.py` files in the current working directory and the `fastui` package directory
3. **Build ID**: On file change, an internal `_build_id` counter is incremented
4. **Browser polling**: An injected JavaScript script polls `GET /_ui/version` every second
5. **Auto-refresh**: When the build ID changes, the script calls `location.reload()`

The injected script looks like:

```javascript
<script>
(function(){
    var v=0;
    setInterval(function(){
        var x=new XMLHttpRequest();
        x.open('GET','/_ui/version',true);
        x.onload=function(){
            var n=parseInt(x.responseText,10);
            if(v&&n!==v)location.reload();
            v=n;
        };
        x.send();
    },1000);
})();
</script>
```

## Console Feedback

When a file changes, the terminal shows:

```
  ♻  changed: main.py
```

## Performance

- Polling interval: 1 second
- File check cost: negligible (`os.stat()` is lightweight)
- No CPU impact during idle periods
- No file system watcher dependencies required

## Limitations

- Only watches `.py` files (not CSS, HTML, or other assets)
- Polling-based (not event-driven like `watchfiles` or `inotify`)
- File changes trigger a full page reload (not partial updates)

## Without Hot Reload

When `hot_reload=False` (default), no polling script is injected and no file watcher
is started. This is the production configuration.

## Next Steps

Continue to [Examples](examples.md) to see complete application examples.
