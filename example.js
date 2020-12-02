const r$ = (v, d$) => v && v.r$ ? d$.push(v.r$) && false : true;
console.log(1 + 2);
(d$ => [
    r$(console.log('hello world'),d$) && 
    r$((d$ => [
        r$(console.log('another message'),d$) && 
        r$({ r$: { r$: 3 } },d$)
    ] && d$.pop())([]),d$) && 
    r$(console.log('escaped message'),d$)
] && d$.pop())([]);