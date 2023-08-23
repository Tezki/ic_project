state(u0).
state(u_acc).
state(u_rej).

all_steps(0..1).
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
ed(u0, u_rej).
trans(u0, u_rej, T) :- rej_cond(T).
#constant(st, u0).
#constant(st, u_acc).
#constant(st, u_rej).

#modeh(ed(const(st),const(st))).
#modeh(trans(const(st),const(st),var(t))).
#modeh(rej_cond(var(t))).

#modeb(1, obs(var(v1),var(t)),(positive)).
#modeb(1, lmk(var(v1))).
#modeb(1, obt(var(v1))).
#modeb(1, bld(var(v1))).
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
    obs(ms, 0).
    last(0).
}).

#pos({reject}, {accept}, {
    obs(mt, 0).
    last(0).
}).

#pos({}, {accept, reject}, {
    obs(sc, 0).
    last(0).
}).

