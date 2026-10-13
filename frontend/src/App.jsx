import { useState } from "react";
import "./App.css";

function App() {
  const [activeTab, setActiveTab] = useState("lost");
  const [itemName, setItemName] = useState("");
  const [description, setDescription] = useState("");
  const [location, setLocation] = useState("");
  const [date, setDate] = useState("");
  const [contact, setContact] = useState("");
  const [message, setMessage] = useState("");
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(false);

  
const API_URL = "https://findit-ai-lost-and-found.onrender.com";


  async function handleSubmit(event) {
    event.preventDefault();

    setMessage("");
    setMatches([]);
    setLoading(true);

    const item = {
      item_name: itemName,
      description,
      location,
      date,
      contact,
      image_url: null,
    };

    try {
      // Step 1: Submit the lost or found item.
      const response = await fetch(
        `${API_URL}/items/${activeTab}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(item),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail
            ? JSON.stringify(data.detail)
            : "Unable to submit item."
        );
      }

      setMessage(
        data.message || "Item submitted successfully!"
      );

      // Step 2: Find matching items in either direction.
      if (data.item_id) {
        const matchEndpoint =
          activeTab === "lost"
            ? `${API_URL}/items/${data.item_id}/matches`
            : `${API_URL}/found-items/${data.item_id}/matches`;

        const matchResponse = await fetch(matchEndpoint);
        const matchData = await matchResponse.json();

        if (!matchResponse.ok) {
          throw new Error(
            matchData.detail ||
              "Item was submitted, but matching failed."
          );
        }

        setMatches(matchData.matches || []);

        // Show an appropriate message when no matches exist.
        if (
          !matchData.matches ||
          matchData.matches.length === 0
        ) {
          setMessage(
            activeTab === "lost"
              ? "Lost item added successfully!"
              : "Found item added successfully!"
          );
        }
      }

      // Step 3: Clear the form after successful submission.
      setItemName("");
      setDescription("");
      setLocation("");
      setDate("");
      setContact("");
    } catch (error) {
      setMessage(
        `Error: ${error.message}. Make sure your backend is running.`
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      {/* Navigation */}
      <header className="navbar">
        <a className="brand" href="#home">
          <span className="brand-icon">🔎</span>
          Find<span className="brand-highlight">It</span>
        </a>

        <nav>
          <a href="#home">Home</a>
          <a href="#report">Report Item</a>
          <a href="#how-it-works">How It Works</a>
        </nav>

        <a href="#report" className="nav-button">
          Get Started →
        </a>
      </header>

      <main id="home">
        {/* Hero Section */}
        <section className="hero">
          <div className="hero-content">
            <div className="badge">
              ✨ AI-POWERED OBJECT MATCHING
            </div>

            <h1>
              Lost something?
              <br />
              <span>Let's find it.</span>
            </h1>

            <p>
              A smarter way to reunite lost belongings with their
              owners. Report an item and let AI help discover
              potential matches.
            </p>

            <div className="hero-buttons">
              <a href="#report" className="primary-button">
                Report an Item →
              </a>

              <a
                href="#how-it-works"
                className="secondary-button"
              >
                How it works
              </a>
            </div>

            <div className="hero-stats">
              <div>
                <strong>AI</strong>
                <span>Smart Matching</span>
              </div>

              <div>
                <strong>24/7</strong>
                <span>Always Accessible</span>
              </div>

              <div>
                <strong>Easy</strong>
                <span>Simple Reporting</span>
              </div>
            </div>
          </div>

          <div className="hero-visual">
            <div className="visual-circle circle-one"></div>
            <div className="visual-circle circle-two"></div>

            <div className="floating-card card-top">
              <span>🎧</span>

              <div>
                <strong>Lost headphones</strong>
                <small>Searching for a match...</small>
              </div>
            </div>

            <div className="search-illustration">
              <div className="illustration-icon">🔍</div>
              <div className="illustration-item">🎒</div>
              <div className="sparkle sparkle-one">✦</div>
              <div className="sparkle sparkle-two">✧</div>
            </div>

            <div className="floating-card card-bottom">
              <span className="match-icon">✓</span>

              <div>
                <strong>Potential match!</strong>
                <small>AI-assisted discovery</small>
              </div>
            </div>
          </div>
        </section>

        {/* Features */}
        <section className="features">
          <div className="feature">
            <div className="feature-icon purple">🤖</div>

            <div>
              <h3>AI-Powered Matching</h3>
              <p>
                Discover similar items through intelligent text
                analysis.
              </p>
            </div>
          </div>

          <div className="feature">
            <div className="feature-icon orange">📍</div>

            <div>
              <h3>Location Based</h3>
              <p>
                Include where an item was lost or found.
              </p>
            </div>
          </div>

          <div className="feature">
            <div className="feature-icon green">🤝</div>

            <div>
              <h3>Reconnect Quickly</h3>
              <p>
                Use contact information to help owners reconnect.
              </p>
            </div>
          </div>
        </section>

        {/* Reporting Form */}
        <section className="report-section" id="report">
          <div className="section-heading">
            <span className="section-label">GET STARTED</span>
            <h2>Let's find what matters.</h2>
            <p>
              Tell us a little about the item you're looking for.
            </p>
          </div>

          <div className="report-card">
            {/* Lost / Found Tabs */}
            <div className="tabs">
              <button
                className={
                  activeTab === "lost"
                    ? "tab active lost"
                    : "tab"
                }
                onClick={() => {
                  setActiveTab("lost");
                  setMessage("");
                  setMatches([]);
                }}
                type="button"
              >
                🔍 I Lost Something
              </button>

              <button
                className={
                  activeTab === "found"
                    ? "tab active found"
                    : "tab"
                }
                onClick={() => {
                  setActiveTab("found");
                  setMessage("");
                  setMatches([]);
                }}
                type="button"
              >
                🎁 I Found Something
              </button>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit}>
              <div className="form-grid">
                <div className="form-group">
                  <label>Item name *</label>

                  <input
                    value={itemName}
                    onChange={(e) =>
                      setItemName(e.target.value)
                    }
                    placeholder="e.g. Black JBL headphones"
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Location *</label>

                  <input
                    value={location}
                    onChange={(e) =>
                      setLocation(e.target.value)
                    }
                    placeholder="e.g. College library"
                    required
                  />
                </div>

                <div className="form-group full-width">
                  <label>Description *</label>

                  <textarea
                    value={description}
                    onChange={(e) =>
                      setDescription(e.target.value)
                    }
                    placeholder="Describe the item, its color, brand, features..."
                    rows="4"
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Date *</label>

                  <input
                    type="date"
                    value={date}
                    onChange={(e) =>
                      setDate(e.target.value)
                    }
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Contact email *</label>

                  <input
                    type="email"
                    value={contact}
                    onChange={(e) =>
                      setContact(e.target.value)
                    }
                    placeholder="you@example.com"
                    required
                  />
                </div>
              </div>

              <button
                className="submit-button"
                type="submit"
                disabled={loading}
              >
                {loading
                  ? "Finding matches..."
                  : activeTab === "lost"
                    ? "Find Matching Items →"
                    : "Find Matching Items →"}
              </button>

              {message && (
                <div className="message" role="status">
                  {message}
                </div>
              )}
            </form>

            {/* Matching Results */}
            {matches.length > 0 && (
              <div className="matches">
                <h3>🎯 Potential Matches</h3>

                <p>
                  {activeTab === "lost"
                    ? "These found items may match your lost item."
                    : "These lost items may match the item you found."}{" "}
                  Verify the details before contacting anyone.
                </p>

                {matches.map((match, index) => (
                  <div
                    className="match-card"
                    key={match.item_id || index}
                  >
                    <div>
                      <h4>{match.item_name}</h4>

                      <p>{match.description}</p>

                      <small>
                        📍 {match.location} · {match.date}
                      </small>
                    </div>

                    <span className="match-score">
                      {match.match_score}% match
                    </span>
                  </div>
                ))}
              </div>
            )}

            {/* No Matches */}
            {message &&
              matches.length === 0 &&
              !loading &&
              message.toLowerCase().includes("success") && (
                <p className="no-matches">
                  {activeTab === "lost"
                    ? "No matching found items were returned. Try again after more found items are reported."
                    : "No matching lost items were returned. Try again after more lost items are reported."}
                </p>
              )}
          </div>
        </section>

        {/* How It Works */}
        <section
          className="how-section"
          id="how-it-works"
        >
          <div className="section-heading">
            <span className="section-label">
              SIMPLE & SMART
            </span>

            <h2>How FindIt works</h2>

            <p>
              Three simple steps to help reunite people with their
              belongings.
            </p>
          </div>

          <div className="steps">
            <div className="step">
              <div className="step-number">01</div>
              <div className="step-emoji">📝</div>
              <h3>Report an Item</h3>
              <p>
                Submit the name, description, date and location.
              </p>
            </div>

            <div className="step">
              <div className="step-number">02</div>
              <div className="step-emoji">🧠</div>
              <h3>AI Finds Matches</h3>
              <p>
                Compare item descriptions using semantic similarity.
              </p>
            </div>

            <div className="step">
              <div className="step-number">03</div>
              <div className="step-emoji">💚</div>
              <h3>Reconnect</h3>
              <p>
                Review possible matches and arrange a safe return.
              </p>
            </div>
          </div>
        </section>

        {/* Call to Action */}
        <section className="cta">
          <h2>
            Every lost item deserves a second chance.
          </h2>

          <p>
            Start your search today with AI-powered assistance.
          </p>

          <a href="#report" className="primary-button">
            Get Started →
          </a>
        </section>
      </main>

      {/* Footer */}
      <footer>
        <a className="brand footer-brand" href="#home">
          🔎 Find<span className="brand-highlight">It</span>
        </a>

        <p>AI Lost and Found Object Matching System</p>

        <span>
          Built to help belongings find their way home. 💜
        </span>
      </footer>
    </div>
  );
}

export default App;