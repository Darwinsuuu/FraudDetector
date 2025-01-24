$(document).ready(() => {
    const apiUrl = "http://127.0.0.1:5000/api/";
    let countdownTimer;
    const rowsPerPage = 8; // Number of rows per page
    let currentPage = 1; // Current active page
    let emailData = []; // Store all email data

    getEmails();

    const spamTips = [
        {
            title: "Verify the Sender's Email Address",
            description: "Always check the sender's email address for any inconsistencies or oddities. Scammers often use email addresses that look similar to legitimate ones but contain small spelling errors or additional characters."
        },
        {
            title: "Be Cautious with Links and Attachments",
            description: "Never click on suspicious links or open attachments from unknown senders. Hover over links to verify they lead to legitimate websites. Scammers often use malicious links to steal personal information or install malware."
        },
        {
            title: "Look for Red Flags in the Message",
            description: "Watch for urgent language, threats, or promises of rewards. Scammers often create a sense of urgency to trick recipients into acting quickly without thinking. Be cautious if the email is asking for sensitive information like passwords, credit card details, or personal data."
        },
        {
            title: "Enable Two-Factor Authentication (2FA)",
            description: "Protect your email and online accounts with 2FA to make it harder for scammers to gain access, even if they have your password. This adds an extra layer of security and helps prevent unauthorized logins."
        },
        {
            title: "Report Suspicious Emails",
            description: "If you receive an email that seems like a scam, report it to your email provider or the company the scammer is pretending to represent. Reporting helps block scammer accounts and prevent future attempts."
        },
    ]


    // Function to get a random tip
    function getRandomTip() {
        const randomIndex = Math.floor(Math.random() * spamTips.length);
        return spamTips[randomIndex];
    }

    // Function to add the random tip to the modal
    function addRandomTipToModal() {
        const randomTip = getRandomTip();
        const tipMessage = document.getElementById('tipMessage');
        tipMessage.innerHTML = `<strong>${randomTip.title}</strong>: ${randomTip.description}`;
    }

    // Add event listener to the submit button
    $("#form").submit((e) => {
        e.preventDefault();

        const emailAddress = $("#emailAddress").val();
        const emailContent = $("#emailContent").val();

        // Create the payload object
        const payload = {
            email_address: emailAddress, // Use `email_address` to match the backend
            email_content: emailContent // Use `email_content` to match the backend
        };

        // Make the AJAX POST request
        $.ajax({
            url: apiUrl + 'spam_detector',
            type: 'POST',
            contentType: 'application/json', // Set content type to JSON
            data: JSON.stringify(payload), // Convert the payload to JSON
            success: function (data) {
                const result = data.result || "Unknown"; // Fallback if the result is missing
                const message = result === "Spam"
                    ? "<h1 class='text-danger fw-bold'>SPAM</h1>"
                    : "<h1 class='text-success fw-bold'>NOT SPAM</h1>";

                $("#resultMessage").html(message);
                const randomNumber = Math.floor(Math.random() * 5);

                // Show the modal
                const spamModal = new bootstrap.Modal(document.getElementById("spamModal"));
                addRandomTipToModal();

                $("#form").trigger("reset");
                spamModal.show();
            },
            error: function (err) {
                if (err.responseJSON && err.responseJSON.error) {
                    console.error('Error:', err.responseJSON.error);
                    alert('An error occurred: ' + err.responseJSON.error);
                } else {
                    console.error('Unknown error:', err);
                    alert('An unknown error occurred.');
                }
            }
        });
    });



    // When the "Get OTP" button is clicked
    $("#getOTP").click(function () {
        let $button = $(this);
        let $message = $("#otpMessage");

        // Disable the button to prevent multiple clicks
        $button.prop("disabled", true);

        // Show the info message (remove the "d-none" class)
        $message.removeClass("d-none").text("Email has been sent!");

        // Set the countdown to 60 seconds
        let countdown = 60;
        $button.text(`Please wait (${countdown}s)`);


        $.ajax({
            url: apiUrl + 'get_otp',
            type: 'GET',
            success: function (data) {
                // Check if OTP was sent successfully
                if (data.status === 'success') {
                    let $button = $("#getOTP");
                    let $message = $("#otpMessage");

                    // Show the info message with the success message from the API
                    $message.removeClass("d-none").text(data.message);

                    // Start countdown
                    let countdown = 60;
                    $button.text(`Please wait (${countdown}s)`);

                    countdownTimer = setInterval(function () {
                        countdown--;
                        $button.text(`Please wait (${countdown}s)`);

                        // Once the countdown reaches 0, enable the button again and hide the message
                        if (countdown === 0) {
                            clearInterval(countdownTimer);
                            $button.prop("disabled", false);
                            $button.text("Get OTP");
                            $message.addClass("d-none");
                        }
                    }, 1000);
                }
            },
            error: function (err) {
                if (err.responseJSON && err.responseJSON.error) {
                    console.error('Error:', err.responseJSON.error);
                    alert('An error occurred: ' + err.responseJSON.error);
                } else {
                    console.error('Unknown error:', err);
                    alert('An unknown error occurred.');
                }
            }
        });
    });




    // Handle login form submission
    $('#loginForm').submit(function (event) {
        event.preventDefault();  // Prevent the default form submission
        var username = $('#username').val();
        var password = $('#password').val();

        if (username && password) {
            // Send login credentials via AJAX to the login API
            $.ajax({
                url: apiUrl + 'login_creds',  // The login endpoint
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    username: username,
                    otp: password  // Assuming the OTP is entered in the 'password' field
                }),
                success: function (response) {
                    if (response.status === 'success') {
                        window.location.href = '/dashboard';
                        // window.location.href = '/';  // Redirect to the home page or dashboard
                    } else {
                        $('#errorMessage').removeClass('d-none').text("Invalid Username or OTP.");
                    }
                },
                error: function (xhr, status, error) {
                    // Print the error message to the console for debugging
                    console.error('AJAX Request Failed:', status, error);
                    console.error('Response:', xhr.responseText);

                    // Display an alert with the error message
                    alert('Error occurred while logging in. Status: ' + status + ', Error: ' + error);
                }
            });
        } else {
            alert('Please fill in all fields.');
        }
    });


    function renderTable() {
        const startDate = $('#start-date-filter').val(); // Get the start date filter
        const endDate = $('#end-date-filter').val(); // Get the end date filter

        // Helper function to format date to YYYY-MM-DD format
        function formatDate(dateString) {
            const date = new Date(dateString);
            return date.toISOString().split('T')[0]; // Returns "YYYY-MM-DD"
        }

        // If start and end dates are provided, filter the data by that range
        const filteredData = emailData.filter(item => {
            const itemDate = formatDate(item.date_created);
            const isInRange =
                (!startDate || itemDate >= startDate) &&
                (!endDate || itemDate <= endDate);
            return isInRange;
        });

        // Calculate start and end indices for slicing the filtered data
        const start = (currentPage - 1) * rowsPerPage;
        const end = start + rowsPerPage;

        // Get the rows for the current page
        const rows = filteredData.slice(start, end);

        // Clear existing rows in the table
        $('#email-table-body').empty();

        // If there are no rows to show (empty filtered result), display a message
        if (rows.length === 0) {
            $('#email-table-body').append('<tr><td colspan="4" class="text-center">No data available for the selected date range.</td></tr>');
        } else {
            // Append rows for the current page
            rows.forEach(function (item) {
                $('#email-table-body').append(`
                    <tr>
                        <td>${item.email}</td>
                        <td>${item.content}</td>
                        <td>${item.spam ? 'Yes' : 'No'}</td>
                        <td>${item.date_created}</td>
                    </tr>
                `);
            });
        }

        // Update pagination after filtering
        renderPagination(filteredData);
    }

    $('#start-date-filter, #end-date-filter').on('change', function () {
        currentPage = 1; // Reset to the first page when changing the filter
        renderTable(); // Re-render table with the selected date range filter
    });

    $('#reset-filter').on('click', function () {
        $('#start-date-filter, #end-date-filter').val(''); // Clear both date filters
        currentPage = 1; // Reset to the first page
        renderTable(); // Re-render the table without any filter
    });

    function renderPagination(filteredData) {
        const totalPages = Math.ceil(filteredData.length / rowsPerPage); // Total number of pages

        // Clear existing pagination controls
        $('#pagination-controls').empty();

        // Generate pagination buttons
        for (let i = 1; i <= totalPages; i++) {
            $('#pagination-controls').append(`
                <li class="page-item ${i === currentPage ? 'active' : ''}">
                    <a class="page-link" href="#" data-page="${i}">${i}</a>
                </li>
            `);
        }

        // Add click event listener to pagination buttons
        $('#pagination-controls .page-link').on('click', function (e) {
            e.preventDefault();
            const selectedPage = parseInt($(this).data('page'));
            if (selectedPage !== currentPage) {
                currentPage = selectedPage;
                renderTable(); // Re-render table with the current filter
            }
        });
    }

    $('#date-filter').on('change', function () {
        currentPage = 1; // Reset to the first page when changing the filter
        renderTable(); // Re-render table with the selected filter
    });

    $('#reset-filter').on('click', function () {
        $('#date-filter').val(''); // Clear the date filter input
        currentPage = 1; // Reset to the first page
        renderTable(); // Re-render the table without any filter
    });

    function getEmails() {
        console.log('Fetching emails...');
        $.ajax({
            url: apiUrl + 'email_data', // Make sure apiUrl is defined correctly
            method: 'GET',
            dataType: 'json',
            success: function (response) {
                emailData = response; // Store the fetched data
                currentPage = 1; // Reset to the first page
                renderTable(); // Render the first page
                renderPagination(emailData); // Render pagination controls
            },
            error: function (error) {
                console.error('Error fetching data:', error);
            }
        });
    }



    $('#download-report').on('click', function () {
        // Prepare the table data for export
        const tableData = [];
        const headers = ['Email', 'Email Content', 'Spam', 'Date Created']; // Define the headers

        // Add the headers to the table data
        tableData.push(headers);

        console.log(emailData)

        // Add the rows from the table body to the table data
        emailData.forEach(item => {
            tableData.push([
                item.email,
                item.content,
                item.spam == 1 ? 'Yes' : 'No',
                item.date_created
            ]);
        });

        // Create a worksheet from the data
        const worksheet = XLSX.utils.aoa_to_sheet(tableData);

        // Create a new workbook and append the worksheet
        const workbook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(workbook, worksheet, 'Emails Report');

        // Generate the Excel file and trigger a download
        XLSX.writeFile(workbook, 'Emails_Report.xlsx');
    });


    $('#logout').on('click', function () {
        Swal.fire({
            title: "Logout",
            text: "Are you sure you want to logout?",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#d33",
            cancelButtonColor: "#3085d6",
            confirmButtonText: "Logout"
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: apiUrl + 'logout',
                    method: 'GET',
                    success: function (response) {
                        if (response.status === 'success') {
                            Swal.fire({
                                title: "Success",
                                text: response.message, // Use the message from the server response
                                icon: "success"
                            }).then(() => {
                                window.location.href = '/';  // Redirect to the home page
                            });
                        }
                    },
                    error: function (error) {
                        Swal.fire({
                            title: "Error",
                            text: "An error occurred while logging out.",
                            icon: "error"
                        });
                        console.error('Error logging out:', error);
                    }
                });
            }
        });
    });





    $('#send-report').on('click', function () {
        Swal.fire({
            title: "Send Report",
            text: "Are you sure you want to send the report to the authorities?",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#007bff",
            cancelButtonColor: "#d33",
            confirmButtonText: "Send Report"
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: apiUrl + 'send_report',
                    method: 'POST',
                    success: function (response) {
                        if (response.status === 'success') {
                            Swal.fire({
                                title: "Success",
                                text: response.message,
                                icon: "success"
                            });
                        } else {
                            Swal.fire({
                                title: "Error",
                                text: response.message,
                                icon: "error"
                            });
                        }
                    },
                    error: function (error) {
                        Swal.fire({
                            title: "Error",
                            text: "An error occurred while sending the report.",
                            icon: "error"
                        });
                        console.error('Error sending report:', error);
                    }
                });
            }
        });
    });


});