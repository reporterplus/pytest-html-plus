import argparse
import base64
import json
import os
import shutil
from datetime import datetime
import html
from sys import path

from pytest_html_plus.compute_filter_counts import compute_filter_count
from pytest_html_plus.utils import extract_trace_block, extract_error_block


def main():
    parser = argparse.ArgumentParser(description="Generate HTML report from Playwright JSON report")
    parser.add_argument("--report", required=True, help="Path to the JSON report file")
    parser.add_argument("--screenshots", default="screenshots", help="Folder path where screenshots are saved")
    parser.add_argument("--output", default="report_output", help="Output folder for HTML report")
    args = parser.parse_args()

    reporter = JSONReporter(
        report_path=args.report,
        screenshots_dir=args.screenshots,
        output_dir=args.output,
    )
    reporter.load_report()
    reporter.generate_html_report()


class JSONReporter:
    def __init__(self, report_path="final_report.json", screenshots_dir="screenshots", output_dir="report_output"):
        self.filters = None
        self.parsed_data = None
        self.report_path = report_path
        self.screenshots_dir = screenshots_dir
        self.output_dir = output_dir
        self.results = []
        all_markers = set()
        for test in self.results:
            for marker in test.get("markers", []):
                all_markers.add(marker)
        all_markers = sorted(all_markers)

    def load_report(self):
        with open(self.report_path) as f:
            data = json.load(f)
        if isinstance(data, dict) and "results" in data:
            self.results = data["results"]
            self.filters = data.get("filters", {})
        elif isinstance(data, list):
            self.results = data
            self.filters = {}
        else:
            raise ValueError("Unexpected report format.")

        metadata_path = os.path.join(os.path.dirname(self.report_path), "plus_metadata.json")
        if os.path.exists(metadata_path):
            with open(metadata_path) as meta_file:
                self.metadata = json.load(meta_file)
        else:
            self.metadata = {}

    def log_result(
            self,
            test_name,
            nodeid,
            status,
            duration,
            trace=None,
            error=None,
            markers=None,
            filepath=None,
            lineno=None,
            stdout=None,
            stderr=None,
            screenshot=None,
            logs=None,
            worker=None,
            links=None
    ):
        result = {
            "test": test_name,
            "nodeid": nodeid,
            "status": status,
            "duration": duration,
            "trace": trace,
            "error": error,
            "markers": markers or [],
            "file": filepath,
            "line": lineno,
            "stdout": stdout,
            "stderr": stderr,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "screenshot": screenshot,
            "logs": logs or [],
            "worker": worker,
            "links": links
        }
        if error:
            result["error"] = error
        self.results.append(result)

    def write_report(self):
        dir_path = os.path.dirname(os.path.abspath(self.report_path))

        # Ensure directory exists
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)


        data = {
            "filters": compute_filter_count(self.results),
            "results": self.results
        }

        try:
            with open(self.report_path, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            raise RuntimeError(f"Failed to write report to '{path}': {e}") from e

    def copy_all_screenshots(self):
        screenshots_output_dir = os.path.join(self.output_dir, "screenshots")
        os.makedirs(screenshots_output_dir, exist_ok=True)
        for root, _, files in os.walk(self.screenshots_dir):
            for file in files:
                if file.endswith(".png"):
                    src_path = os.path.join(root, file)
                    dest_path = os.path.join(screenshots_output_dir, file)
                    if not os.path.exists(dest_path):
                        shutil.copyfile(src_path, dest_path)

    def find_screenshot_and_copy(self, test_name):
        screenshots_output_dir = os.path.join(self.output_dir, "screenshots")
        os.makedirs(screenshots_output_dir, exist_ok=True)

        # We'll look for any .png file where test_name is contained in the filename (partial match)
        for root, _, files in os.walk(self.screenshots_dir):
            for file in files:
                if file.endswith(".png") and test_name in file:
                    src_path = os.path.join(root, file)

                    dest_path = os.path.join(screenshots_output_dir, file)

                    shutil.copyfile(src_path, dest_path)

                    # Return relative path from output_dir for HTML src
                    return os.path.join("screenshots", file)
        return None

    def generate_copy_button(self, content, label):
        if isinstance(content, list):
            # Convert list to string (for logs)
            content_str = '\n'.join(str(item) for item in content)
        elif content is None:
            content_str = ""
        else:
            content_str = str(content)
            
        # Encode content as base64 to avoid any JavaScript syntax issues
        content_b64 = base64.b64encode(content_str.encode('utf-8')).decode('ascii')
        return f"""<button class="inline-copy-btn" onclick="event.stopPropagation(); copyFromBase64('{content_b64}', this)" title="Copy {label}">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                    </svg>
                </button>
            """

    def generate_html_report(self):
        # Extract all unique markers
        ignore_markers = {"link"}
        all_markers = set()
        for test in self.results:
            for marker in test.get("markers", []):
                if marker not in ignore_markers:
                    all_markers.add(marker)

        html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <style>
    
      body {{ font-family: Arial, sans-serif; padding: 1rem; background: #f9f9f9; }}
      .test {{ border: 1px solid #ddd; margin-bottom: 0.5rem; border-radius: 5px; background: white; }}
      .header {{ padding: 0.5rem; cursor: pointer; display: flex; justify-content: space-between; align-items: center; gap: 8px; flex-wrap: wrap; }}
      .header.passed {{ background: #e6f4ea; color: #2f7a33; }}
      .header.failed {{ background: #fdecea; color: #a83232; }}
      .header.skipped {{  background: #fff8e1; color: #b36b00;  }}
      .header.error {{  background: #f0f0f0; color: #f0f0f0;  }}
      .details {{ padding: 0.5rem 1rem; display: none; border-top: 1px solid #ddd; }}
      .toggle::before {{ content: "▶"; display: inline-block; margin-right: 0.5rem; transition: transform 0.3s ease; }}
      .header.expanded .toggle::before {{ transform: rotate(90deg); }}
      .checkbox-container {{ margin-bottom: 1rem; display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center; }}
      .details-content {{ display: flex; gap: 1rem; align-items: flex-start; }}
      .details-text {{ flex: 1; min-width: 0; }}
      .details-screenshot {{ flex-shrink: 0; margin: 1rem; box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.1); }}
      .details-screenshot img {{width: 300px; height: 200px; object-fit: contain; border: 1px solid #ccc; border-radius: 3px; background: #f8f8f8; cursor: pointer; transition: transform 0.2s ease; transform: scale(1.05); }}
      .details-screenshot img:hover {{  transform: scale(1.05); }}
      
      /* Handle content wrapping */
      .details-text {{ 
        word-wrap: break-word;
        overflow-wrap: break-word;
      }}
      
      /* Special handling for links and pre-formatted text */
      .details-text a {{ 
        word-break: break-all; 
      }}
      .details-text pre {{ 
        white-space: pre-wrap;
        max-width: 100%;
        word-break: break-all;  
      }}
    
      /* Mobile and tablet responsiveness */
      @media (max-width: 768px) {{
        .header {{ flex-direction: column; align-items: stretch; gap: 0.5rem; }}
        .header-section {{ justify-content: space-between; }}
        .test-info {{ min-width: auto; }}
        .meta {{ flex-direction: column; gap: 0.25rem; }}
        .badges-and-timing {{ justify-content: flex-start; flex-wrap: wrap; }}
        .badges-and-timing > * {{ margin-left: 0; margin-right: 0.5rem; }}
        
        .details-content {{ flex-direction: column; gap: 0.5rem; }}
        .details-screenshot {{ align-self: center; }}
        .details-screenshot img {{ width: 100%; max-width: 300px; height: auto; min-height: 150px; }}
        
        /* For Mobile URL handling */
        .header a {{ max-width: 100px; }}
        .nodeid-badge code {{ max-width: 200px; }}
      }}
      
      @media (max-width: 480px) {{
        .header {{ padding: 0.75rem 0.5rem; }}
        .details {{ padding: 0.5rem; }}
        .test-info strong {{ font-size: 0.9rem; }}
        .nodeid-badge code {{ font-size: 0.5em; }}
        .worker-id {{ font-size: 0.75em; }}
        .timestamp {{ font-size: 0.85em; }}
        
        .details-screenshot img {{ max-width: 100%; height: auto; min-height: 120px; }}
        
        .checkbox-container {{ flex-direction: column; gap: 0.5rem; }}
        .checkbox-container label {{ margin-left: 0 !important; }}
      }}
      .details-screenshot img.fullscreen {{ position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%) scale(1); width: auto; height: auto; max-width: 90vw; max-height: 90vh; z-index: 1000; background: white; box-shadow: 0 4px 20px rgba(0,0,0,0.5); border-radius: 8px; }}
      .fullscreen-overlay {{ position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.8); z-index: 999; display: none; }}  
      .search-container {{ margin-bottom: 1rem; }}
      .search-container input {{ box-sizing: border-box; }}
      .header-section {{ display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }}
      .test-info {{ flex: 1; min-width: 200px; word-break: break-word; white-space: normal; }}
      .meta {{ justify-content: flex-start; flex: 1; word-break: break-word; white-space: normal; }}
      .badges-and-timing {{ justify-content: flex-end; flex-wrap: wrap; }}
      .timestamp {{ white-space: nowrap; font-weight: bold; }}
      .badges-and-timing > * {{ margin-left: 24px; }}
      
      /* Handle long URLs in header links */
      .header a {{ word-break: break-all; overflow-wrap: break-word; max-width: 150px; display: inline-block; }}
      .nodeid-badge code {{ word-break: break-all; overflow-wrap: break-word; max-width: 300px; }}
      
      .inline-copy-btn {{ cursor: pointer; background: none; border: 1px solid #ddd; border-radius: 3px; padding: 2px 4px; font-size: 0.8em; margin-left: 8px; color: #666; transition: all 0.2s ease; line-height: 1; }} 
      .inline-copy-btn:hover {{ border-color: #999; background: #f5f5f5; color: #333; }}
      .error-content pre {{ background: #fef2f2; border-left: 4px solid #dc2626; padding: 12px; border-radius: 4px; color: #7f1d1d; margin: 8px 0; }}
      .trace-content pre {{ background: #fef7ed; border-left: 4px solid #ea580c; padding: 12px; border-radius: 4px; color: #9a3412; margin: 8px 0; }}
      .details-text div pre {{ background: #f8fafc; border: 1px solid #e2e8f0; padding: 12px; border-radius: 4px; margin: 8px 0; font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace; font-size: 0.85em; line-height: 1.4; }}
      .details-text div strong {{ display: inline-flex; align-items: center; gap: 8px; margin-bottom: 8px; font-weight: 600; color: #374151; }}
      .trace-content strong, .error-content strong {{ margin-bottom: 12px; }}
      .report-metadata {{
        margin-bottom: 5px;
        font-family: sans-serif;
        background: #f9f9f9;
        border: 1px solid #ddd;
        border-radius: 3px;
        padding: 5px;
    }}

    .report-metadata summary {{
        font-size: 0.5em;
        cursor: pointer;
        margin-bottom: 5px;
    }}

    .report-metadata table {{
        width: 100%;
        border-collapse: collapse;
    }}

    .report-metadata th, .report-metadata td {{
        text-align: left;
        padding: 8px;
        border-bottom: 1px solid #ddd;
    }}

    .report-metadata th {{
        background-color: #eee;
        width: 200px;
    }}
    .hidden {{ display: none; }}
    </style>

    <script>
      function toggleDetails(headerElem) {{
        headerElem.classList.toggle('expanded');
        const details = headerElem.nextElementSibling;
        details.style.display = (details.style.display === 'block') ? 'none' : 'block';
      }}

      function copyFromBase64(base64Content, button) {{
        try {{
          const originalContent = button.innerHTML;
          // Decode base64 content for copy
          const decodedContent = atob(base64Content);
          navigator.clipboard.writeText(decodedContent).then(() => {{
            button.innerHTML = '<span style="color: #2f7a33;">✓</span>';
            setTimeout(() => {{
              button.innerHTML = originalContent;
            }}, 1000);
          }}).catch(err => {{
            console.error("Copy failed:", err);
            button.innerHTML = '<span style="color: #d32f2f;">✗</span>';
            setTimeout(() => {{
              button.innerHTML = originalContent;
            }}, 1000);
          }});
        }} catch (error) {{
          console.error("Copy button error:", error);
        }}
      }}

      function toggleFullscreen(img) {{
        const overlay = document.getElementById('fullscreen-overlay');
        if (img.classList.contains('fullscreen')) {{
          img.classList.remove('fullscreen');
          overlay.style.display = 'none';
          document.body.style.overflow = 'auto';
        }} else {{
          img.classList.add('fullscreen');
          overlay.style.display = 'block';
          document.body.style.overflow = 'hidden';
        }}
      }}

      function closeFullscreen() {{
        const fullscreenImg = document.querySelector('.details-screenshot img.fullscreen');
        const overlay = document.getElementById('fullscreen-overlay');
        
        if (fullscreenImg) {{
          fullscreenImg.classList.remove('fullscreen');
          overlay.style.display = 'none';
          document.body.style.overflow = 'auto';
        }}
      }}


      function toggleFilter(longestCheckbox) {{
        const failedCheckbox = document.getElementById('failedOnlyCheckbox');
        const skippedCheckbox = document.getElementById('skippedOnlyCheckbox');
        const untrackedCheckbox = document.getElementById('untrackedOnlyCheckbox');
        const flakyCheckbox = document.getElementById('flakyOnlyCheckbox');
        const testsContainer = document.getElementById('tests-container');
        const testElements = Array.from(testsContainer.querySelectorAll('.test'));

        if (longestCheckbox.checked) {{
          failedCheckbox.checked = false;
          skippedCheckbox.checked = false;
          untrackedCheckbox.checked = false;
          flakyCheckbox.checked = false;
          // Re-enable all tests before sorting
          testElements.forEach(el => el.style.display = 'block');

          // Sort and reorder
          testElements.sort((a, b) => {{
            const aDuration = parseFloat(
        a.querySelector('.timestamp').textContent.replace(/[^\d.]/g, '')
        ) || 0;
            const bDuration = parseFloat(b.querySelector('.timestamp').textContent.replace(/[^\d.]/g, '')) || 0;
            return bDuration - aDuration;
          }});

          testElements.forEach(el => testsContainer.appendChild(el));
        }}

        // Reapply marker filter (should now handle failed/skipped too)
        filterByMarkers();
      }}

      function toggleUntrackedOnly(checkbox) {{
        const testCards = document.querySelectorAll('.test-card');
        const longestCheckbox = document.getElementById('longestOnlyCheckbox');
        const skippedCheckbox = document.getElementById('skippedOnlyCheckbox');
        const failedCheckbox = document.getElementById('failedOnlyCheckbox');
        const flakyCheckbox = document.getElementById('flakyOnlyCheckbox');

        if (checkbox.checked) {{
          longestCheckbox.checked = false;
          skippedCheckbox.checked = false;
          failedCheckbox.checked = false;
          flakyCheckbox.checked = false
          testCards.forEach(card => {{
            const hasLink = card.querySelector('a[href]');
            card.style.display = hasLink ? 'none' : 'block';
          }});
        }} else {{
          testCards.forEach(card => {{
            card.style.display = 'block';
          }});
        }}
      }}

      function toggleUntrackedInfo() {{
        const card = document.getElementById('untrackedInfoCard');
        card.style.display = card.style.display === 'none' ? 'block' : 'none';
      }}

      function toggleFlakyOnly(checkbox) {{
          const longestCheckbox = document.getElementById('longestOnlyCheckbox');
          const untrackedCheckbox = document.getElementById('untrackedOnlyCheckbox');
          const skippedCheckbox = document.getElementById('skippedOnlyCheckbox');
          const failedCheckbox = document.getElementById('failedOnlyCheckbox');
        const testElements = document.querySelectorAll('.test');
        if (checkbox.checked) {{
          longestCheckbox.checked = false;
          skippedCheckbox.checked = false;
          failedCheckbox.checked = false;
          untrackedCheckbox.checked = false;
          testElements.forEach(el => {{
            const isFlaky = el.querySelector('.is-flaky') !== null;
            el.style.display = isFlaky ? 'block' : 'none';
          }});
        }} else {{
          testElements.forEach(el => {{
            el.style.display = 'block';
          }});
        }}
      }}

      function toggleFailedOnly(failedCheckbox) {{
        const longestCheckbox = document.getElementById('longestOnlyCheckbox');
        const untrackedCheckbox = document.getElementById('untrackedOnlyCheckbox');
        const skippedCheckbox = document.getElementById('skippedOnlyCheckbox');
        const flakyCheckbox = document.getElementById('flakyOnlyCheckbox');
        const testElements = document.querySelectorAll('.test');
        if (failedCheckbox.checked) {{
          longestCheckbox.checked = false;
          untrackedCheckbox.checked = false;
          skippedCheckbox.checked = false;
          flakyCheckbox.checked = false;
          testElements.forEach(el => {{
            const header = el.querySelector('.header');
            const isFailed = header.classList.contains('failed');
            el.style.display = isFailed ? 'block' : 'none';
          }});
        }} else {{
          testElements.forEach(el => el.style.display = 'block');
        }}
        filterByMarkers(); // Reapply marker filter
      }}

      function toggleSkippedOnly(skippedCheckbox) {{
        const longestCheckbox = document.getElementById('longestOnlyCheckbox');
        const failedCheckbox = document.getElementById('failedOnlyCheckbox');
        const untrackedCheckbox = document.getElementById('untrackedOnlyCheckbox');
        const flakyCheckbox = document.getElementById('flakyOnlyCheckbox');
        const testElements = document.querySelectorAll('.test');

        if (skippedCheckbox.checked) {{
          longestCheckbox.checked = false;
          failedCheckbox.checked = false;
          untrackedCheckbox.checked = false;
          flakyCheckbox.checked = false;
          testElements.forEach(el => {{
            const header = el.querySelector('.header');
            const isSkipped = header.classList.contains('skipped');
            el.style.display = isSkipped ? 'block' : 'none';
          }});
        }} else {{
          testElements.forEach(el => el.style.display = 'block');
        }}

        filterByMarkers(); // Reapply marker filter
      }}

      function initializeUniversalSearch() {{
          const searchInput = document.getElementById('universal-search');
          if (!searchInput) return;

          searchInput.addEventListener('input', function (e) {{
              const filter = e.target.value.toLowerCase();
              document.querySelectorAll('.test-card').forEach(card => {{
                  const name = card.getAttribute('data-name') || '';
                  const link = card.getAttribute('data-link') || '';
                  const isVisible = name.toLowerCase().includes(filter) || link.toLowerCase().includes(filter);
                  card.style.display = isVisible ? '' : 'none';
              }});
          }});
        }}

      document.addEventListener('DOMContentLoaded', initializeUniversalSearch);

      function filterByMarkers() {{
        const selected = Array.from(document.querySelectorAll('.marker-filter input[type="checkbox"]:checked')).map(cb => cb.value);
        const failedOnly = document.getElementById('failedOnlyCheckbox').checked;
        const skippedOnly = document.getElementById('skippedOnlyCheckbox').checked;

        document.querySelectorAll('.test').forEach(el => {{
          const header = el.querySelector('.header');
          const markers = el.getAttribute('data-markers').split(',');
          const isFailed = header.classList.contains('failed');
          const isSkipped = header.classList.contains('skipped');

          const showAllMarkers = selected.length === 0;
          const matchesMarker = showAllMarkers || selected.some(m => markers.includes(m));
          const matchesFailed = !failedOnly || isFailed;
          const matchesSkipped = !skippedOnly || isSkipped;

          el.style.display = (matchesMarker && matchesFailed && matchesSkipped) ? 'block' : 'none';
        }});
      }}


      window.onload = function() {{
        const failedCheckbox = document.getElementById('failedOnlyCheckbox');
        const longestCheckbox = document.getElementById('longestOnlyCheckbox');
        const skippedCheckbox = document.getElementById('skippedOnlyCheckbox');
        const untrackedCheckbox = document.getElementById('untrackedOnlyCheckbox');
        const flakyCheckbox = document.getElementById('flakyOnlyCheckbox');
        failedCheckbox.checked = true;
        toggleFailedOnly(failedCheckbox);
        failedCheckbox.addEventListener('change', () => toggleFailedOnly(failedCheckbox));
        longestCheckbox.addEventListener('change', () => toggleFilter(longestCheckbox));
        skippedCheckbox.addEventListener('change', () => toggleSkippedOnly(skippedCheckbox));
        untrackedCheckbox.addEventListener('change', () => toggleUntrackedOnly(untrackedCheckbox));
        flakyCheckbox.addEventListener('change', () => toggleFlakyOnly(flakyCheckbox));
        const markerCheckboxes = document.querySelectorAll('.marker-filter input[type="checkbox"]');
        markerCheckboxes.forEach(cb => cb.addEventListener('change', filterByMarkers));
      }};
    </script>
    </head>
    <body>
    <div class="report-metadata">
    <h2 onclick="this.nextElementSibling.classList.toggle('hidden')" style="cursor: pointer; font-size: 12px;">
        Execution Metadata (click to toggle)
         {self.generate_copy_button(self.metadata, "metadata")}
    </h2>
    <table class="hidden" style="margin-top:10px;">
        <tr><th>Title</th><td>{self.metadata.get('report_title', '')}</td></tr>
        <tr><th>Environment</th><td>{self.metadata.get('environment', '')}</td></tr>
        <tr><th>Branch</th><td>{self.metadata.get('branch', '')}</td></tr>
        <tr><th>Commit</th><td>{self.metadata.get('commit', '')}</td></tr>
        <tr><th>Generated At</th><td>{self.metadata.get('generated_at', '')}</td></tr>
        <tr><th>Python version</th><td>{self.metadata.get('python_version', '')}</td></tr>
    </table>
</div>
    <div id="fullscreen-overlay" class="fullscreen-overlay" onclick="closeFullscreen()"></div>
    <div class="checkbox-container">
      <label>
        <input type="checkbox" id="failedOnlyCheckbox" />
        Show only failed tests (<span>{self.filters.get("failed", 0)}</span>)
      </label>
      <label>
        <input type="checkbox" id="skippedOnlyCheckbox" />
        Show only skipped tests (<span>{self.filters.get("skipped", 0)}</span>)
      </label>
      <label style="margin-left: 1rem;">
        <input type="checkbox" id="longestOnlyCheckbox" />
        Sort by longest running tests
      </label>
      <label style="margin-left: 1rem;">
        <input type="checkbox" id="untrackedOnlyCheckbox" />
        Show untracked (<span>{self.filters.get("untracked", 0)}</span>)
      </label>
      <span onclick="toggleUntrackedInfo()" style="
  display: inline-flex;
  justify-content: center;
  align-items: center;
  width: 18px;
  height: 18px;
  margin-left: 6px;
  background-color: #3498db;
  color: white;
  border-radius: 50%;
  font-size: 12px;
  font-weight: bold;
  cursor: pointer;
  user-select: none;
" title="What is untracked?">i</span>

<div id="untrackedInfoCard" style="
  display: none;
  background: #f9f9f9;
  color: #333;
  border: 1px solid #ccc;
  border-radius: 6px;
  padding: 10px 14px;
  margin-top: 8px;
  max-width: 400px;
  font-size: 0.85em;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
">
  <strong>Untracked Tests:</strong><br>
  These tests do not have any associated tracking markers like:
  <ul style="margin: 6px 0 0 16px; padding: 0;">
    <li><code>pytest.mark.link("https://...")</code></li>
    <li><code>pytest.mark.jira("PROJ-123")</code></li>
    <li><code>pytest.mark.issue("https://...")</code></li>
    <li><code>pytest.mark.testcase("https://...")</code></li>
  </ul>
  Add these markers to your test to track them better
</div>
<label style="margin-left: 1rem;">
  <input type="checkbox" id="flakyOnlyCheckbox">
  Show flaky tests only (<span>{self.filters.get("flaky", 0)}</span>)
</label>
    </div>
    <div class="search-container">
          <input
  type="text"
  id="universal-search"
  placeholder="🔍 Search by anything, testname? link ids?..."
  style="width: 100%; padding: 10px; margin-bottom: 20px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px;"
/>
    </div>


    <div id="markersFilter" class="marker-filter" style="margin-bottom: 1rem;">
      <strong>Filter by Markers:</strong><br/>
    """


        # Add checkboxes for all markers
        marker_counts = self.filters.get("marker_counts", {})
        for marker in sorted(marker_counts):
            count = marker_counts[marker]
            html += f'<label><input type="checkbox" value="{marker}" /> {marker} ({count})</label> '

        html += '<div id="tests-container">'

        # Generate test blocks
        for test in self.results:
            status_class = (
                'passed' if test['status'] == 'passed' else
                'failed' if test['status'] == 'failed' else
                'skipped'
            )
            screenshot_path = self.find_screenshot_and_copy(test['test'])
            screenshot_html = f'<div class="details-screenshot"><img src="{screenshot_path}" alt="Screenshot" onclick="toggleFullscreen(this)"></div>' if screenshot_path else ""
            markers = test.get("markers")
            marker_str = ",".join(markers) if isinstance(markers, list) else ""
            stdout_html = ""
            if test.get('stdout'):
                stdout_escaped = test['stdout'].replace("`", "\\`")  # Escape backticks
                stdout_html = f"""
                <div><strong>STDOUT:</strong> {self.generate_copy_button(stdout_escaped, 'stdout')}
                <pre>{test['stdout']}</pre></div>
                """

            stderr_html = ""
            if test.get('stderr'):
                stderr_escaped = test['stderr'].replace("`", "\\`")
                stderr_html = f"""
                <div><strong>STDERR:</strong> {self.generate_copy_button(stderr_escaped, 'stderr')}
                <pre>{test['stderr']}</pre></div>
                """

            logs_html = ""
            logs_content = test.get('logs')
            if logs_content:
                if isinstance(logs_content, list):
                    logs_display = '\n'.join(str(item) for item in logs_content if item)
                else:
                    logs_display = str(logs_content)
                if logs_display.strip():
                    logs_html = f"""
                    <div><strong>Logs:</strong> {self.generate_copy_button(logs_content, 'logs')}
                    <pre>{logs_display}</pre></div>
                    """

            trace_html = ""
            error_html = ""
            
            if test.get('error'):
                full_error = test['error']
                full_trace = test['trace']
                trace_content = extract_trace_block(full_trace)
                error_content = extract_error_block(full_error)
                
                if trace_content and trace_content.strip():
                    trace_html = f"""
                    <div class="trace-content"><strong>Trace:</strong> {self.generate_copy_button(trace_content, 'trace')}
                    <pre>{trace_content}</pre></div>
                    """
                
                if error_content and error_content.strip():
                    error_html = f"""
                    <div class="error-content"><strong>Error:</strong> {self.generate_copy_button(error_content, 'error')}
                    <pre>{error_content}</pre></div>
                    """

            flaky_badge = ""
            if test.get("flaky"):
                flaky_badge = (
                    '<span class="is-flaky" '
                    'style="background:#f39c12;color:white;padding:2px 6px;'
                    'border-radius:3px;font-weight:bold;font-size:0.85em;">FLAKY</span>'
                )
            else:
                 # Invisible placeholder to preserve layout
                flaky_badge = '<span style="display:inline-block; min-width:40px;"></span>'

            link_html = ""
            links = test.get("links", [])
            if links:
                for url in links:
                    link_html += (
                        f'<a href="{url}" target="_blank" '
                        f'style="background:#3498db;color:white;padding:2px 6px;'
                        f'border-radius:3px;font-weight:bold;font-size:0.85em;'
                        f'text-decoration:none;margin-right:6px;"> Link </a>'
                    )
            else:
              # Invisible placeholder to preserve layout
              link_html = '<span style="display:inline-block; min-width:45px;"></span>'

            html += f'''
    
<div class="test test-card" data-name="{test['test']}" data-link="{','.join(test.get('links') or [])}" data-markers="{marker_str}">
  <div class="header {status_class}" onclick="toggleDetails(this)">
    <div class="header-section test-info">
      <span class="toggle"></span>
      <strong>{test["test"]}</strong>
      <span>— {test["status"].upper()}</span>
    </div>
    <div class="header-section meta">
      <span class="nodeid-badge" style="display: flex; align-items: center; gap: 6px;">
        <code style="font-size: 0.6em; color: #555;">{test["nodeid"]}</code>
          {self.generate_copy_button(test["nodeid"], "nodeid")}
      </span>
      <span class="worker-id" style="background: #ddd; border-radius: 3px; padding: 2px 5px; font-size: 0.85em; font-weight: bold;">{test["worker"]}</span>
    </div>

    <div class="header-section badges-and-timing">
      {flaky_badge}
      {link_html}
      <span class="timestamp">⏱ {test.get("duration", 0):.2f}s</span>
    </div>
  </div>

  <div class="details">
    <div class="details-content">
      <div class="details-text">
         {error_html}
        {trace_html}
        {stdout_html}
        {stderr_html}
        {logs_html}
      </div>
      {screenshot_html}
    </div>
  </div>
</div>

    '''

        # Add summary
        total_tests = len(self.results)
        failed_tests = sum(1 for t in self.results if t['status'] == 'failed')
        error_tests = sum(1 for t in self.results if t['status'] == 'error')
        slowest_test = max(self.results, key=lambda x: x.get('duration', 0), default=None)
        slowest_test_name = slowest_test['test'] if slowest_test else 'N/A'
        slowest_test_duration = slowest_test.get('duration', 0) if slowest_test else 0

        summary_html = f"""
            <div style="padding: 1rem; background: {'#e6f4ea' if failed_tests == 0 and error_tests == 0 else '#fdecea'}; 
            border: 1px solid {'#2f7a33' if failed_tests == 0 and error_tests == 0 else '#a83232'}; 
            border-radius: 5px; margin-bottom: 1rem;">
              {'<strong>Bingo!</strong> All your tests passed!' if failed_tests == 0 and error_tests == 0 else
        f'Total tests: {total_tests}, Failures: {failed_tests}, Errors: {error_tests}.'}
              The slowest test was <strong>{slowest_test_name}</strong> at {slowest_test_duration:.2f}s.
            </div>
            """

        html = html.replace('<div id="tests-container">', summary_html + '<div id="tests-container">')
        html += "</div></body></html>"

        # Save report
        os.makedirs(self.output_dir, exist_ok=True)
        output_file = os.path.join(self.output_dir, "report.html")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)

if __name__ == "__main__":
    main()
