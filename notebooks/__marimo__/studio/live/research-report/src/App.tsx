/// <reference path="./marimo-studio.d.ts" />

import { Deck, Slide } from "@revealjs/react";
import { useEffect, useRef } from "react";
import type { RevealApi } from "reveal.js";
import "reveal.js/reveal.css";

const keyboardCondition = (event: KeyboardEvent) =>
  !event.composedPath().some(
    (target) =>
      target instanceof Element && target.matches("marimo-cell, marimo-output"),
  );

/** Center slides again once projected notebook content has its final size. */
const useSettledLayout = () => {
  const deck = useRef<RevealApi | null>(null);
  useEffect(() => {
    const layout = () => deck.current?.layout();
    document.addEventListener("marimo-studio:idle", layout);
    return () => document.removeEventListener("marimo-studio:idle", layout);
  }, []);
  return deck;
};

export const App = () => {
  const deck = useSettledLayout();
  return (
    <Deck
      className="studio-deck"
      deckRef={deck}
      config={{
        controls: true,
        keyboardCondition,
        progress: true,
        scrollActivationWidth: 0,
        transition: "slide",
      }}
    >
      <Slide>
        <div className="nes-container is-rounded slide-frame">
          <h1>IRED88 Deep Mutational Scan Analysis</h1>
          <div className="slide-chart">
            <marimo-cell name="dms_activity_heatmap" />
          </div>
          <div className="slide-sentence">
            <marimo-output value="heatmap_lead" />
          </div>
        </div>
      </Slide>
      <Slide>
        <div className="nes-container is-rounded slide-frame">
          <div className="slide-chart slide-chart-standout">
            <marimo-output value="position_dive" />
          </div>
        </div>
      </Slide>
      <Slide>
        <div className="nes-container is-rounded slide-frame">
          <div className="slide-viewer">
            <marimo-cell name="structure_viewer" />
          </div>
        </div>
      </Slide>
    </Deck>
  );
};
