import pytest
from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
from deepeval.test_case import LLMTestCase

CONTEXT = """
EXECUTIVE PLAN OF COURSE TEACHING Course code and name 87243, INF007 Software engineering Teacher Associate assistant. Ph.D. Nikola Tanković (instructor) Study program University undergraduate study Informatics Type of course Compulsory Course level Undergraduate Semester Winter Year of study III. Place of performance Hall 402, new building of FET "Dr. Mijo Mirković" Language of instruction Croatian Number of ECTS credits 6.0 Number of hours per semester 30P - 30V - 0S Prerequisites for enrollment and mastering Courses taken Programming, Databases I, Advanced programming techniques Correlativity Programming, Databases I, Databases II, Structures data and algorithms, Advanced programming techniques, Web applications. The aim of the course is to acquaint students with modern techniques for developing software applications and systems.   Master applicable paradigms, programming languages, libraries and frameworks for developing software solutions.  Learning outcomes 1. Collect and analyze user requirements 2. Apply the UML language in system design 3. Explain and apply different architectural styles 4. Apply at least two programming languages ​​and one application development framework 5. Apply the agile method in software development 6. Apply methods for testing software support and form a system of continuous testing 7. Teamwork to develop a complete software solution and related documentation that meets functional and non-functional requirements Course content 1. Introduction to software engineering. Software product development methods with an emphasis on agile methods. 2. Gathering requirements and system prototyping. 3. System modeling using the UML language. UML models. 4. Javascript programming language. The Vue framework. 5. Cloud application implementation using Vue/Javascript framework and Firebase service.
The structure of the study "Management of Business Processes" at the undergraduate study of Informatics includes a course called "Management of Business Processes" (UPPFIPU) which is conducted in the winter semester of the third year of study in Pula. The course carries 6 ECTS points and consists of 30 hours of lectures and 30 hours of exercises. There are no prerequisites for enrolling in the course, but it is necessary to pass the "Fundamentals of ICT" course to access the test or exam.
The aim of the course is to acquire competencies for business process management, business process model design and application of business process analysis methods using modern programming tools and frameworks. Learning outcomes include describing the issues of business process management, explaining the role of information systems, applying optimal ways of managing business processes, comparing reference models and methodological frameworks, and using BPMN, UML and Petri Nets methods for modeling business processes.

Required reading for the course includes the works "Business Process Modeling" by Brumec, J. and Brumec, S. (2018) and "Fundamentals of Business Process Management" by Dumas, M. et al. (2013). Optional literature includes the works "Business Process Management: Concepts, Languages, Architectures" by Weska, M. (2012) and "Management of business processes – organizational and informational approach" by Bosilj-Vukšić, V., Hernaus, T., Kovačić, A (2008).

Additionally, for the "Software Engineering" course, recommended reading includes "Professional Software Development" by Mike G. Miller (2020), "Software Engineering Body of Knowledge (SWEBOK)" by IEEE (2014), "Clean Architecture: A Craftsman's Guide to Software Structure and Design" by Robert C. Martin (2017) and "Beginning Software Engineering" by Rod Stephens (2015). Optional reading includes "Software Engineering at Google: Lessons Learned from Programming Over Time" by Titues Winters, Tom Manshreck, Hyrum Wright (2020), while reference reading includes "Eloquent JavaScript" by Marijn Haverbeke (2019), "Learning Vue.js 2 " by Olga Filipova (2016) and "Version Control with Git" by Jon Loeliger (2012).
Study structure BUSINESS PROCESS MANAGEMENT
Management of business processes
Course code and name: 199739, Business Process Management (UPPFIPU)
Teachers
associate professor Ph.D. Darko Etinger (holder)
Dario Kukuljan, mag. paed. et educ. inf.
Information about the course
Study program: Informatics (undergraduate)
Course type: compulsory
Course level: undergraduate
Semester: winter
Year of study: III.
Place of performance: Pula
Language of performance: Croatian, English
Number of ECTS credits: 6
Number of hours per semester: 30P - 30V - 0S
Correlativity:
Faculty of Organization and Informatics Varaždin: Modeling business processes
Zagreb Faculty of Economics: Business Process Management
Prerequisites:
There are no prerequisites for enrolling in the course.
The prerequisite for taking the test or applying for the exam is to have previously completed the ICT Basics course.
Objective of the course
Acquire competencies for business process management, design of business process models and application of methods
for analyzing business processes using modern programming tools and frameworks.
Learning outcomes
1. Describe the issue of business process management, interpret the basic features, advantages and disadvantages
sufficient process approach.
2. Explain the role of an integral information system and a system for managing business processes, u
achieving a higher level of process maturity.
3. Apply the optimal way of managing business processes based on analysis and presentation, improve
measurement and application of the concept of process maturity.
4. To compare reference models and methodological frameworks that facilitate the implementation of business change projects
process.
5. Use BPMN, UML and Petri Nets methods for modeling business processes.
6. Apply software tools for design and analysis of business processes.
Course content
1. Process approach - orientation to business processes.
2. Process-oriented organization.
3. Business process analysis, business process management.
4. Knowledge in business processes and information systems.
5. Organizational and informational approach to the development of business process management systems.
6. Methods of business process modeling and company model development.
7. BPMN - Business process model and notation
Page 214
Course "Program Engineering" at the University Undergraduate Study of Informatics, led by Assoc. Ph.D. Nikola Tanković, is required for the third year of study in the winter semester. The course is held in hall 402 of the new FET building "Dr. Mijo Mirković" in the Croatian language and has 6 ECTS credits. Prerequisites for admission include completed courses Programming, Databases I and Advanced Programming Techniques. The aim of the course is to acquaint students with modern techniques for developing software applications and systems, and to master applicable paradigms, programming languages, libraries and frameworks.

Studenti su obvezni pohađati nastavu, izraditi projektni zadatak, pristupiti kontrolnim zadaćama i usmenom ispitu. Projektni zadatak nosi 50% ocjene, kontrolne zadaće 10%, a usmeni ispit 40%. Da bi položili kolegij, studenti moraju ostvariti najmanje 50% bodova putem aktivnosti kontinuiranog praćenja ili pristupiti završnom ispitu.
6. Tools for managing versions of program code. The Git tool, the GitHub service, and the collaborative development process. 7. Data storage systems in the cloud Firebase Firestore and Storage. 8. Verification of program support. Unit tests and end-to-end type tests. A system for continuous software integration.
Planned activities, learning and teaching methods and assessment methods Obligations Outcomes Hours ECTS Maximum share in the grade (%) Attendance at classes 1-6 28 1.0 0% Project 1-7 98 3.5 50% Control tasks 1-6 14 0, 5 10% Oral exam 1-6 28 1.0 40% Total 168 6.0 100% Additional clarifications (evaluation criteria): Class attendance: During lectures, students are presented with concepts related to the development of distributed multi-layer applications and are illustrated with practical examples through exercises in the computer laboratory.   Project assignment: Students are required to independently choose the topic of project assignments approved by the teacher. The thematic framework and the required amount of functionality will be defined in advance. When creating a project assignment, it is possible to independently choose the used programming languages ​​and frameworks. The project task needs to be realized through two components: the application prototype and the application itself. Students are required to place the created project on one of the source code version management systems, which will be used to monitor the progress in building the project, and additionally place a link to the source code in the designated place on e-learning. A successfully defended project carries a maximum of 50 points, of which 5 points refer to the prototype, 20 points to the client components, 20 points to the server components and 5 points to the presentation of the project. Using someone else's solution (plagiarism) is prohibited and entails disciplinary liability.  Control tasks: During the course, knowledge tests will be conducted, which will proportionally contribute to the final points in the maximum amount of 10%. Each check consists in realizing the required functionality using script languages ​​and libraries covered in previous lectures.  Oral exam: At the oral exam in the last week of classes, knowledge of the presented course material is determined in accordance with the learning outcomes. It is possible to earn up to 40% points.  The exam is passed if the student achieves at least 50% points through continuous monitoring activities during the semester. The assessment of continuous monitoring is based on the achieved points according to the following scale:
The text provides basic information about variables and operators in JavaScript, including the rules for declaring variables with `const', different data types, and the use of strings and exponential notation. Explains basic operators such as arithmetic, association, comparison, logical, and type operators, and their uses. JavaScript is used to create interactive web pages, as well as server-side, desktop and mobile applications. There are three ways to write JavaScript code in a web browser: inline, internal, and external JavaScript.

The structure of the study "Management of Business Processes" at the undergraduate study of Informatics includes the course "Management of Business Processes" which is conducted in the winter semester of the third year in Pula. The course carries 6 ECTS credits, consists of 30 hours of lectures and 30 hours of exercises, and there are no prerequisites for enrollment, but it is necessary to pass the "Fundamentals of ICT" course. The goal of the course is the acquisition of competencies for business process management, the design of business process models, and the application of business process analysis methods using modern tools and frameworks.

"""

ACTUAL_OUTPUT = """
Dear student, the course codes "Business Process Management" and "Software Engineering" are equivalent to 6 ECTS credits.
"""


EXPECTED_OUTPUT= """
The course code "Business Process Management" is 199739, and the course code "Software Engineering" is 87243.
"""

def test_case():
    answer_relevancy_metric = AnswerRelevancyMetric(threshold=0.5)
    faithfulness_metric = FaithfulnessMetric(threshold=0.5)
    test_case = LLMTestCase(
        input="What are the course codes for Business Process Management and Software Engineering?",
        actual_output=ACTUAL_OUTPUT,
        expected_output=EXPECTED_OUTPUT,
        retrieval_context=[CONTEXT]
    )
    assert_test(test_case, [answer_relevancy_metric, faithfulness_metric])

if __name__ == "__main__":
    test_case()
