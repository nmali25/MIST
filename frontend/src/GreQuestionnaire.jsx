import React, { useState, useEffect } from "react";
import "./GreQuestionnaire.css";

const TOTAL_TIME_SECONDS = 10 * 60; // 10 minutes

const QUESTIONS = [
  {
    id: 1,
    question: "If 4x - 8 = 12, what is the value of x?",
    options: [
      { id: "A", text: "3", isCorrect: false },
      { id: "B", text: "4", isCorrect: false },
      { id: "C", text: "5", isCorrect: true },
      { id: "D", text: "6", isCorrect: false },
    ],
    hint: "Add 8 to both sides and divide by 4.",
    explanation: "4x - 8 = 12 → 4x = 20 → x = 5.",
  },
  {
    id: 2,
    question: "A price increases from ₹80 to ₹100. What is the percent increase?",
    options: [
      { id: "A", text: "15%", isCorrect: false },
      { id: "B", text: "20%", isCorrect: false },
      { id: "C", text: "25%", isCorrect: true },
      { id: "D", text: "30%", isCorrect: false },
    ],
    hint: "Percent increase = (increase ÷ original) × 100.",
    explanation: "Increase = 20. Percent = (20/80)×100 = 25%.",
  },
  {
    id: 3,
    question: "What is 3/4 + 1/2?",
    options: [
      { id: "A", text: "5/4", isCorrect: true },
      { id: "B", text: "7/4", isCorrect: false },
      { id: "C", text: "3/8", isCorrect: false },
      { id: "D", text: "1", isCorrect: false },
    ],
    hint: "Convert 1/2 to 2/4.",
    explanation: "3/4 + 2/4 = 5/4.",
  },
  {
    id: 4,
    question: "The ratio of boys to girls is 3:2. If there are 15 boys, how many girls are there?",
    options: [
      { id: "A", text: "8", isCorrect: false },
      { id: "B", text: "10", isCorrect: true },
      { id: "C", text: "12", isCorrect: false },
      { id: "D", text: "14", isCorrect: false },
    ],
    hint: "3 parts → 15, so 1 part = 5.",
    explanation: "Girls = 2 parts × 5 = 10.",
  },
  {
    id: 5,
    question: "A box has 2 red and 3 blue balls. What is the probability of picking a red ball?",
    options: [
      { id: "A", text: "1/2", isCorrect: false },
      { id: "B", text: "2/5", isCorrect: true },
      { id: "C", text: "3/5", isCorrect: false },
      { id: "D", text: "1/3", isCorrect: false },
    ],
    hint: "Probability = red / total.",
    explanation: "Total = 5. Red = 2. So probability = 2/5.",
  },
];

export default function GreQuestionnaire() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedOptionId, setSelectedOptionId] = useState(null);
  const [showHint, setShowHint] = useState(false);
  const [showResult, setShowResult] = useState(false);
  const [score, setScore] = useState(0);
  const [answeredCount, setAnsweredCount] = useState(0);
  const [timeLeft, setTimeLeft] = useState(TOTAL_TIME_SECONDS);
  const [isExamOver, setIsExamOver] = useState(false);

  const currentQuestion = QUESTIONS[currentIndex];

  // Global exam timer
  useEffect(() => {
    if (isExamOver) return;

    const intervalId = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(intervalId);
          setIsExamOver(true);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(intervalId);
  }, [isExamOver]);

  const formatTime = (seconds) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    const mm = m.toString().padStart(2, "0");
    const ss = s.toString().padStart(2, "0");
    return `${mm}:${ss}`;
  };

  const handleOptionClick = (optionId) => {
    if (showResult || isExamOver) return;
    setSelectedOptionId(optionId);
  };

  const isCorrectSelected = () => {
    if (!selectedOptionId) return false;
    const selected = currentQuestion.options.find(
      (opt) => opt.id === selectedOptionId
    );
    return selected?.isCorrect;
  };

  const handleSubmit = () => {
    if (!selectedOptionId || showResult || isExamOver) return;

    const correct = isCorrectSelected();
    if (correct) {
      setScore((prev) => prev + 1);
    }
    setAnsweredCount((prev) => prev + 1);
    setShowResult(true);
  };

  const handleNext = () => {
    if (isExamOver) return;

    const last = currentIndex === QUESTIONS.length - 1;
    if (!last) {
      setCurrentIndex((prev) => prev + 1);
      setSelectedOptionId(null);
      setShowHint(false);
      setShowResult(false);
    } else {
      // Finished all questions before time
      setIsExamOver(true);
    }
  };

  const handleRetake = () => {
    setCurrentIndex(0);
    setSelectedOptionId(null);
    setShowHint(false);
    setShowResult(false);
    setScore(0);
    setAnsweredCount(0);
    setTimeLeft(TOTAL_TIME_SECONDS);
    setIsExamOver(false);
  };

  const percentage =
    QUESTIONS.length > 0 ? Math.round((score / QUESTIONS.length) * 100) : 0;

  const timeUsed = TOTAL_TIME_SECONDS - timeLeft;

  return (
    <div className="gre-container">
      <div className="gre-card">
        <div className="gre-header">
          <div>
            <h2>GRE Quant Mini Test</h2>
            <span className="gre-progress">
              {isExamOver
                ? "Exam finished"
                : `Question ${currentIndex + 1} of ${QUESTIONS.length}`}
            </span>
          </div>
          <div
            className={`gre-timer ${
              timeLeft <= 30 && !isExamOver ? "danger" : ""
            }`}
          >
            ⏱ {formatTime(timeLeft)}
          </div>
        </div>

        {isExamOver ? (
          // ======= SUMMARY VIEW =======
          <div className="gre-summary">
            <h3>Score Summary</h3>
            <div className="summary-grid">
              <div className="summary-stat">
                <span className="label">Score</span>
                <span className="value">
                  {score} / {QUESTIONS.length}
                </span>
              </div>
              <div className="summary-stat">
                <span className="label">Accuracy</span>
                <span className="value">{percentage}%</span>
              </div>
              <div className="summary-stat">
                <span className="label">Questions attempted</span>
                <span className="value">
                  {answeredCount} / {QUESTIONS.length}
                </span>
              </div>
              <div className="summary-stat">
                <span className="label">Time used</span>
                <span className="value">{formatTime(timeUsed)}</span>
              </div>
            </div>

            <p className="summary-note">
              {timeLeft === 0
                ? "Time is up! Review your weak areas and try again."
                : "Nice! You finished before time. You can retake the test to improve your score."}
            </p>

            <button className="retake-btn" onClick={handleRetake}>
              Retake Test
            </button>
          </div>
        ) : (
          // ======= QUESTION VIEW =======
          <>
            <div className="gre-question-text">
              {currentQuestion.question}
            </div>

            <div className="gre-options">
              {currentQuestion.options.map((option) => {
                const isSelected = selectedOptionId === option.id;
                const isCorrect = option.isCorrect;

                let optionClass = "gre-option";
                if (showResult) {
                  if (isSelected && isCorrect) optionClass += " correct";
                  else if (isSelected && !isCorrect) optionClass += " wrong";
                } else if (isSelected) {
                  optionClass += " selected";
                }

                return (
                  <button
                    key={option.id}
                    className={optionClass}
                    onClick={() => handleOptionClick(option.id)}
                  >
                    <span className="option-label">{option.id}.</span>
                    <span>{option.text}</span>
                  </button>
                );
              })}
            </div>

            <div className="gre-actions">
              <button
                className="hint-btn"
                onClick={() => setShowHint((prev) => !prev)}
              >
                {showHint ? "Hide Hint" : "Show Hint"}
              </button>

              {!showResult ? (
                <button
                  className="submit-btn"
                  disabled={!selectedOptionId}
                  onClick={handleSubmit}
                >
                  Check Answer
                </button>
              ) : (
                <button className="next-btn" onClick={handleNext}>
                  {currentIndex === QUESTIONS.length - 1
                    ? "Finish"
                    : "Next"}
                </button>
              )}
            </div>

            {showHint && (
              <div className="hint-box">
                <strong>Hint:</strong> {currentQuestion.hint}
              </div>
            )}

            {showResult && (
              <div
                className={`result-box ${
                  isCorrectSelected() ? "ok" : "bad"
                }`}
              >
                {isCorrectSelected()
                  ? "✅ Correct!"
                  : "❌ Wrong. Check the explanation:"}
                <p className="explanation">
                  <strong>Explanation:</strong>{" "}
                  {currentQuestion.explanation}
                </p>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
