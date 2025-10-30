import json
import xml.etree.ElementTree as ET

def sanitize_classname(filepath):
    if not filepath:
        return "default"
    return filepath.replace("\\", ".").replace("/", ".").removesuffix(".py")

def sanitize_test_name(test):
    return test.get("test") or test.get("nodeid", "unknown").split("::")[-1]

def convert_json_to_junit_xml(json_path, xml_path):
    with open(json_path, "r", encoding="utf-8") as f:
         payload = json.load(f)

    if not isinstance(payload, dict):
        raise RuntimeError(f"Invalid report format: expected JSON object at top-level in {json_path}")

    if "results" not in payload:
        raise RuntimeError(f"Invalid report format: missing 'results' key in {json_path}")

    test_results = payload["results"]

    if not isinstance(test_results, list):
        raise RuntimeError(f"Invalid report format: 'results' must be a list in {json_path}")


    testsuite = ET.Element("testsuite", {
        "name": "Test Suite",
        "tests": str(len(test_results)),
    })

    for test in test_results:
        testcase = ET.SubElement(testsuite, "testcase", {
            "classname": sanitize_classname(test.get("file")),
            "name": sanitize_test_name(test),
            "time": str(test.get("duration", 0)),
        })

        if test.get("timestamp"):
            testcase.set("timestamp", test["timestamp"])
        if test.get("line") is not None:
            testcase.set("line", str(test["line"]))
        if test.get("worker"):
            testcase.set("worker", test["worker"])
        if test.get("flaky") is not None:
            testcase.set("flaky", str(test["flaky"]).lower())

        # Add status tag
        status = test.get("status", "").lower()
        if status == "failed":
            failure = ET.SubElement(testcase, "failure", {
                "message": test.get("error") or "Test failed",
                "type": "AssertionError"
            })
            failure.text = test.get("stderr", "")
        elif status == "skipped":
            ET.SubElement(testcase, "skipped")

        # Add stdout/stderr
        if test.get("stdout"):
            system_out = ET.SubElement(testcase, "system-out")
            system_out.text = test["stdout"]
        if test.get("stderr"):
            system_err = ET.SubElement(testcase, "system-err")
            system_err.text = test["stderr"]

        # Add <properties>
        properties = ET.SubElement(testcase, "properties")

        # Markers
        for marker in test.get("markers", []):
            ET.SubElement(properties, "property", {
                "name": "marker",
                "value": marker
            })

        # Links
        for link in test.get("links", []):
            ET.SubElement(properties, "property", {
                "name": "link",
                "value": link
            })

        # Screenshot
        if test.get("screenshot"):
            ET.SubElement(properties, "property", {
                "name": "screenshot",
                "value": test["screenshot"]
            })

        # Logs
        for log in test.get("logs", []):
            ET.SubElement(properties, "property", {
                "name": "log",
                "value": str(log)
            })

    try:
        tree = ET.ElementTree(testsuite)
        tree.write(xml_path, encoding="utf-8", xml_declaration=True)
    except OSError as e:
        raise RuntimeError(f"Failed to write XML report to {xml_path}: {e}") from e
