// Minimal reactive store: one-way data flow.
// setState replaces the state and notifies subscribers (no external mutation).

export function createStore(initialState) {
  let state = { ...initialState };
  const subscribers = new Set();

  function getState() {
    return state;
  }

  function setState(partial) {
    state = { ...state, ...partial };
    subscribers.forEach((listener) => listener(state));
  }

  function subscribe(listener) {
    subscribers.add(listener);
    return () => subscribers.delete(listener);
  }

  return { getState, setState, subscribe };
}
