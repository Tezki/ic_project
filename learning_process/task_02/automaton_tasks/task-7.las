state(u0).
state(u_acc).
state(u_rej).

all_steps(0..56).
step(T) :- all_steps(T), last(U), T<U+1.

st(0, u0).
st(T+1, Y) :- st(T, X), delta(X, Y, T).

accept :- last(T), st(T+1, u_acc).
reject :- last(T), st(T+1, u_rej).

phi(X, Y, T) :- trans(X, Y, T), ed(X, Y), step(T).
out_phi(X, T) :- phi(X, _, T).
delta(X, Y, T) :- phi(X, Y, T).
delta(X, X, T) :- not out_phi(X, T), state(X), step(T).

reachable(u0).
reachable(Y) :- reachable(X), ed(X, Y).
:- not reachable(X), state(X).

path(X, Y) :- ed(X, Y).
path(X, Y) :- ed(X, Z), path(Z, Y).
:- path(X, Y), path(Y, X).

:- trans(X, Y1, T), trans(X, Y2, T), Y1!=Y2.

lmk(ms). lmk(wf). lmk(cv). lmk(pk). 
obt(ft). obt(wf). obt(mt). obt(ml). 
bld(ms). bld(sc). bld(ch). bld(ml). 
eq(V,C) :- lmk(V), lmk(C), V==C.
eq(V,C) :- lmk(V), obt(C), V==C.
eq(V,C) :- lmk(V), bld(C), V==C.
eq(V,C) :- obt(V), lmk(C), V==C.
eq(V,C) :- obt(V), obt(C), V==C.
eq(V,C) :- obt(V), bld(C), V==C.
eq(V,C) :- bld(V), lmk(C), V==C.
eq(V,C) :- bld(V), obt(C), V==C.
eq(V,C) :- bld(V), bld(C), V==C.

ed(u0, u_rej).
trans(u0, u_rej, T) :- rej_cond(T).
#constant(st, u0).
#constant(st, u_acc).
#constant(st, u_rej).

#constant(o, ms).
#constant(o, wf).
#constant(o, cv).
#constant(o, pk).
#constant(o, ft).
#constant(o, wf).
#constant(o, mt).
#constant(o, ml).
#constant(o, ms).
#constant(o, sc).
#constant(o, ch).
#constant(o, ml).
#modeh(ed(const(st),const(st))).
#modeh(trans(const(st),const(st),var(t))).
#modeh(rej_cond(var(t))).

#modeb(1, obs(var(v1),var(t)),(positive)).
#modeb(1, lmk(var(v1))).
#modeb(1, obt(var(v1))).
#modeb(1, bld(var(v1))).
#modeb(1, eq(var(v1),const(o))).
#modeb(1, rej_cond(var(t)),(negative)).

#bias("
:- not head(_).

:- head(ed(U,U)).
:- head(ed(U,_)), U=u_acc.
:- head(ed(U,_)), U=u_rej.
:- head(ed(_,U)), U=u_rej.
:- head(ed(U1,U2)), body(B).

:- head(trans(U,U,T)).
:- head(trans(U,_,T)), U=u_acc.
:- head(trans(U,_,T)), U=u_rej.
:- head(trans(_,U,T)), U=u_rej.

:- body(lmk(V)), not body(obs(V,_)).
:- body(naf(lmk(V))), not body(obs(V,_)).
:- body(obt(V)), not body(obs(V,_)).
:- body(naf(obt(V))), not body(obs(V,_)).
:- body(bld(V)), not body(obs(V,_)).
:- body(naf(bld(V))), not body(obs(V,_)).
:- body(eq(V,C)), not body(obs(V,_)).
:- body(naf(eq(V,C))), not body(obs(V,_)).

:- head(trans(U1,U2,T)), not body(naf(rej_cond(T))).
:- head(trans(U1,U2,T1)), body(naf(rej_cond(T2))), T1!=T2.
:- head(rej_cond(T)), body(rej_cond(_)).
").

#maxv(2).
#pos({accept}, {reject}, {
    obs(pk, 0).
    last(0).
}).

#pos({accept}, {reject}, {
    obs(sc, 0). obs(sc, 1). obs(sc, 2). obs(sc, 3). obs(sc, 4). obs(sc, 5). obs(sc, 6). obs(sc, 7). obs(sc, 8). obs(sc, 9). obs(sc, 10). obs(sc, 11). obs(sc, 12). obs(sc, 13). obs(sc, 14). obs(sc, 15). obs(sc, 16). obs(sc, 17). obs(sc, 18). obs(sc, 19). obs(sc, 20). obs(sc, 21). obs(sc, 22). obs(sc, 23). obs(sc, 24). obs(sc, 25). obs(sc, 26). obs(sc, 27). obs(sc, 28). obs(sc, 29). obs(sc, 30). obs(sc, 31). obs(sc, 32). obs(sc, 33). obs(sc, 34). obs(sc, 35). obs(sc, 36). obs(sc, 37). obs(sc, 38). obs(sc, 39). obs(sc, 40). obs(sc, 41). obs(sc, 42). obs(sc, 43). obs(sc, 44). obs(sc, 45). obs(sc, 46). obs(sc, 47). obs(sc, 48). obs(sc, 49). obs(sc, 50). obs(sc, 51). obs(sc, 52). obs(sc, 53). obs(sc, 54). obs(cv, 55).
    last(55).
}).

#pos({reject}, {accept}, {
    obs(ft, 0).
    last(0).
}).

#pos({reject}, {accept}, {
    obs(ml, 0).
    last(0).
}).

#pos({}, {accept, reject}, {
    obs(ms, 0).
    last(0).
}).

#pos({}, {accept, reject}, {
    obs(mt, 0).
    last(0).
}).

#pos({}, {accept, reject}, {
    obs(sc, 0).
    last(0).
}).

